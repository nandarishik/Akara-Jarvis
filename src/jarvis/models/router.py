from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

import httpx

from jarvis.config import Settings
from jarvis.db import store
from jarvis.models.providers import (
    DEFAULT_BASE_URLS,
    ResolvedEndpoint,
    any_provider_key,
    api_key_for,
    chat_completions,
)
from jarvis.models.registry import ModelRegistry
from jarvis.models.routing import MODEL_TO_CHAIN, ModelRouting, ProviderFallbacks


class BudgetExceeded(Exception):
    pass


@dataclass
class ResolvedModel:
    agent: str
    model_key: str
    provider: str
    model_id: str
    base_url: str
    api_key: str
    temperature: float
    openhands_model: str | None = None


def _repo_config_dir(settings: Settings) -> Path:
    raw = Path(settings.model_config_dir)
    if raw.is_absolute() and raw.is_dir():
        return raw
    # Prefer CWD (project root when running jarvis), then walk up from package
    candidates = [
        Path.cwd() / raw,
        Path(__file__).resolve().parents[3] / raw,
        Path(__file__).resolve().parents[2] / raw,
    ]
    for c in candidates:
        if (c / "model-routing.yaml").is_file():
            return c
    return candidates[0]


class ModelRouter:
    def __init__(self, settings: Settings, conn) -> None:
        self.settings = settings
        self.conn = conn
        self.config_dir = _repo_config_dir(settings)
        self.registry = ModelRegistry(self.config_dir)
        self.routing = ModelRouting(self.config_dir)
        self.fallbacks = ProviderFallbacks(self.config_dir)

    def has_credentials(self) -> bool:
        return any_provider_key(self.settings)

    def resolve(self, agent: str, *, high_risk: bool = False) -> ResolvedModel:
        cfg = self.routing.agent_config(agent)
        model_key = self.routing.select_model_key(agent, high_risk=high_risk)
        temperature = float(cfg.get("temperature") or 0.2)
        if high_risk:
            temperature = float(
                self.routing.global_rules.get("temperature_for_security_sensitive")
                or 0.0
            )
        endpoint = self._pick_endpoint(model_key)
        oh = (cfg.get("openhands_settings") or {}).get("model")
        if high_risk and cfg.get("escalation_model"):
            # Prefer OpenHands string for default; escalation may lack openhands model
            oh = oh or None
        return ResolvedModel(
            agent=agent,
            model_key=model_key,
            provider=endpoint.provider,
            model_id=endpoint.model_id,
            base_url=endpoint.base_url,
            api_key=endpoint.api_key,
            temperature=temperature,
            openhands_model=str(oh) if oh else None,
        )

    def openhands_model(self, agent: str, *, high_risk: bool = False) -> tuple[str, str]:
        """Return (LiteLLM/OpenHands model string, api_key).

        Prefer routing YAML openhands_settings; use OpenRouter key when the
        model string is openrouter/... (typical Phase 1 path).
        """
        cfg = self.routing.agent_config(agent)
        oh_settings = cfg.get("openhands_settings") or {}
        resolved = self.resolve(agent, high_risk=high_risk)
        model_str = oh_settings.get("model")
        if high_risk and resolved.model_key != cfg.get("default_model"):
            model_str = oh_settings.get("fallback_model_openhands") or model_str
        if not model_str:
            entry = self.registry.provider_entry(resolved.model_key, "openrouter")
            slug = (entry or {}).get("model_id") or resolved.model_id
            model_str = slug if str(slug).startswith("openrouter/") else f"openrouter/{slug}"
        model_str = str(model_str)
        or_key = api_key_for(self.settings, "openrouter")
        if model_str.startswith("openrouter/") and or_key:
            return model_str, or_key
        return model_str, resolved.api_key

    def _pick_endpoint(self, model_key: str) -> ResolvedEndpoint:
        hops = self.fallbacks.chain_for_model(model_key)
        errors: list[str] = []
        for hop in hops:
            provider = str(hop.get("provider") or "")
            if provider == "HALT":
                break
            key = api_key_for(self.settings, provider)
            if not key:
                errors.append(f"{provider}: no api key")
                continue
            model_id = str(
                hop.get("model_id")
                or hop.get("pinned_model_id")
                or ""
            )
            base = str(hop.get("base_url") or DEFAULT_BASE_URLS.get(provider) or "")
            if not model_id or not base:
                # fill from registry
                entry = self.registry.provider_entry(model_key, provider)
                if entry:
                    model_id = model_id or str(
                        entry.get("pinned_model_id") or entry.get("model_id") or ""
                    )
                    base = base or str(entry.get("api_base_url") or "")
            if not model_id or not base:
                errors.append(f"{provider}: missing model_id/base_url")
                continue
            return ResolvedEndpoint(
                provider=provider,
                model_id=model_id,
                base_url=base,
                api_key=key,
                model_key=model_key,
            )
        # Last resort: OpenRouter with registry openrouter slug if key present
        or_key = api_key_for(self.settings, "openrouter")
        if or_key:
            entry = self.registry.provider_entry(model_key, "openrouter")
            if entry and entry.get("model_id"):
                return ResolvedEndpoint(
                    provider="openrouter",
                    model_id=str(entry["model_id"]),
                    base_url=DEFAULT_BASE_URLS["openrouter"],
                    api_key=or_key,
                    model_key=model_key,
                )
        chain = MODEL_TO_CHAIN.get(model_key, "?")
        raise RuntimeError(
            f"no usable provider for model={model_key} chain={chain}: "
            + "; ".join(errors)
            or "no hops"
        )

    def _estimate_usd(
        self, model_key: str, provider: str, prompt_tokens: int, completion_tokens: int
    ) -> float:
        entry = self.registry.provider_entry(model_key, provider) or {}
        inp = float(entry.get("input_price_per_million") or 0.3)
        out = float(entry.get("output_price_per_million") or 1.2)
        return (prompt_tokens / 1_000_000) * inp + (completion_tokens / 1_000_000) * out

    def complete(
        self,
        *,
        agent: str,
        messages: list[dict[str, str]],
        task_id: UUID | None,
        correlation_id: UUID | None,
        budget_remaining: int,
        high_risk: bool = False,
        tier: int | None = None,  # retained for callers; ignored for dispatch
    ) -> tuple[str, int]:
        del tier  # agent-based dispatch
        if not self.has_credentials():
            raise RuntimeError(
                "No LLM API keys configured. Set OPENROUTER_API_KEY and/or "
                "DEEPSEEK_API_KEY / MINIMAX_API_KEY / etc."
            )
        cfg = self.routing.agent_config(agent)
        model_key = self.routing.select_model_key(agent, high_risk=high_risk)
        temperature = float(cfg.get("temperature") or 0.2)
        if high_risk:
            temperature = float(
                self.routing.global_rules.get("temperature_for_security_sensitive")
                or 0.0
            )

        hops = self.fallbacks.chain_for_model(model_key)
        last_err: Exception | None = None
        tried: list[str] = []

        def try_endpoint(ep: ResolvedEndpoint) -> tuple[str, int]:
            text, prompt_tokens, completion_tokens, cost = chat_completions(
                base_url=ep.base_url,
                api_key=ep.api_key,
                model_id=ep.model_id,
                messages=messages,
                temperature=temperature,
                provider=ep.provider,
            )
            total = prompt_tokens + completion_tokens
            if total > budget_remaining:
                raise BudgetExceeded(
                    f"call used {total} tokens; remaining budget {budget_remaining}"
                )
            usd = (
                float(cost)
                if cost is not None
                else self._estimate_usd(
                    ep.model_key, ep.provider, prompt_tokens, completion_tokens
                )
            )
            today = store.today_spend(self.conn)
            would_pause = (today + usd) >= self.settings.daily_spend_cap_usd
            store.log_llm_call(
                self.conn,
                task_id=task_id,
                correlation_id=correlation_id,
                agent=agent,
                model=ep.model_id,
                source=ep.provider,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                usd_estimate=usd,
                would_pause=would_pause,
            )
            return text, total

        for hop in hops:
            provider = str(hop.get("provider") or "")
            if provider == "HALT":
                break
            key = api_key_for(self.settings, provider)
            if not key:
                continue
            model_id = str(hop.get("model_id") or "")
            base = str(hop.get("base_url") or DEFAULT_BASE_URLS.get(provider) or "")
            entry = self.registry.provider_entry(model_key, provider)
            if entry:
                model_id = model_id or str(
                    entry.get("pinned_model_id") or entry.get("model_id") or ""
                )
                base = base or str(entry.get("api_base_url") or "")
            if not model_id or not base:
                continue
            ep = ResolvedEndpoint(
                provider=provider,
                model_id=model_id,
                base_url=base,
                api_key=key,
                model_key=model_key,
            )
            tried.append(provider)
            try:
                return try_endpoint(ep)
            except BudgetExceeded:
                raise
            except (httpx.HTTPError, httpx.TimeoutException, OSError) as exc:
                last_err = exc
                continue

        # OpenRouter last resort from registry
        or_key = api_key_for(self.settings, "openrouter")
        if or_key and "openrouter" not in tried:
            entry = self.registry.provider_entry(model_key, "openrouter")
            if entry and entry.get("model_id"):
                ep = ResolvedEndpoint(
                    provider="openrouter",
                    model_id=str(entry["model_id"]),
                    base_url=DEFAULT_BASE_URLS["openrouter"],
                    api_key=or_key,
                    model_key=model_key,
                )
                try:
                    return try_endpoint(ep)
                except BudgetExceeded:
                    raise
                except (httpx.HTTPError, httpx.TimeoutException, OSError) as exc:
                    last_err = exc

        raise RuntimeError(
            f"all providers failed for model={model_key} tried={tried}: {last_err}"
        )
