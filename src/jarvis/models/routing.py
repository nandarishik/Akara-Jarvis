from __future__ import annotations

import fnmatch
from pathlib import Path
from typing import Any

import yaml

# Graph / Task.agent short names ? Portfolio B routing keys
AGENT_ALIASES: dict[str, str] = {
    "jarvis": "jarvis_orchestrator",
    "orchestrator": "jarvis_orchestrator",
    "product": "product_agent",
    "architect": "architect_agent",
    "design": "design_agent",
    "frontend": "frontend_agent",
    "backend": "backend_agent",
    "ai_ml": "ai_ml_agent",
    "aiml": "ai_ml_agent",
    "database": "database_agent",
    "code_review": "code_review_agent",
    "review": "code_review_agent",
    "qa": "qa_agent",
    "security": "security_agent",
    "devops": "devops_agent",
    "documentation": "documentation_agent",
    "docs": "documentation_agent",
}

# model registry key ? fallback chain name in provider-fallbacks.yaml
MODEL_TO_CHAIN: dict[str, str] = {
    "deepseek_v4_pro": "deepseek_v4_pro_chain",
    "deepseek_v4_flash": "deepseek_v4_flash_chain",
    "minimax_m3": "minimax_m3_chain",
    "glm_5_2": "glm_5_2_chain",
    "kimi_k2_7_code": "kimi_k2_7_code_chain",
    "kimi_k3": "kimi_k3_chain",
    "devstral_small_2505": "devstral_small_chain",
    "gpt_oss_120b": "gpt_oss_120b_chain",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"missing model config: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"invalid YAML root in {path}")
    return data


class ModelRouting:
    def __init__(self, config_dir: Path) -> None:
        self.raw = _load_yaml(config_dir / "model-routing.yaml")
        self.agents: dict[str, Any] = dict(self.raw.get("agents") or {})
        self.risk = dict(self.raw.get("risk_classifier") or {})
        self.global_rules = dict(self.raw.get("global_rules") or {})

    def routing_key(self, agent: str) -> str:
        key = agent.strip().lower().replace("-", "_").replace(" ", "_")
        if key in self.agents:
            return key
        aliased = AGENT_ALIASES.get(key)
        if aliased and aliased in self.agents:
            return aliased
        # allow passing full key
        if f"{key}_agent" in self.agents:
            return f"{key}_agent"
        raise KeyError(f"no routing entry for agent={agent!r}")

    def agent_config(self, agent: str) -> dict[str, Any]:
        return dict(self.agents[self.routing_key(agent)])

    def select_model_key(self, agent: str, *, high_risk: bool = False) -> str:
        cfg = self.agent_config(agent)
        if high_risk:
            for field in (
                "high_risk_model",
                "escalation_model",
                "high_risk_reviewer_model",
            ):
                val = cfg.get(field)
                if val:
                    return str(val)
        return str(cfg["default_model"])

    def is_high_risk(
        self,
        *,
        paths: list[str] | None = None,
        task_description: str = "",
        content: str = "",
    ) -> bool:
        high = self.risk.get("high_risk_patterns") or {}
        paths = paths or []
        for pattern in high.get("file_path_patterns") or []:
            for path in paths:
                if fnmatch.fnmatch(path.replace("\\", "/"), pattern):
                    return True
        text = f"{task_description}\n{content}".lower()
        for kw in high.get("task_description_keywords") or []:
            if str(kw).lower() in text:
                return True
        for pat in high.get("content_patterns") or []:
            if str(pat).lower() in text:
                return True
        return False


class ProviderFallbacks:
    def __init__(self, config_dir: Path) -> None:
        self.raw = _load_yaml(config_dir / "provider-fallbacks.yaml")
        self.chains: dict[str, Any] = dict(self.raw.get("model_family_chains") or {})

    def chain_for_model(self, model_key: str) -> list[dict[str, Any]]:
        chain_name = MODEL_TO_CHAIN.get(model_key)
        if not chain_name or chain_name not in self.chains:
            # Soft fallback: openrouter-only hop if chain missing
            return []
        chain = self.chains[chain_name]
        hops = chain.get("priority_ordered_providers") or []
        return [h for h in hops if isinstance(h, dict) and h.get("provider") != "HALT"]
