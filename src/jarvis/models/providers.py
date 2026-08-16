from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

# provider id ? Settings attribute / env name
PROVIDER_KEY_ATTR: dict[str, str] = {
    "deepseek_official": "deepseek_api_key",
    "minimax_official": "minimax_api_key",
    "zai_official": "zai_api_key",
    "moonshot_official": "moonshot_api_key",
    "mistral_official": "mistral_api_key",
    "openrouter": "openrouter_api_key",
    "deepinfra": "deepinfra_api_key",
    "groq": "groq_api_key",
    "fireworks_ai": "fireworks_api_key",
    "cerebras": "cerebras_api_key",
}

DEFAULT_BASE_URLS: dict[str, str] = {
    "deepseek_official": "https://api.deepseek.com",
    "minimax_official": "https://api.minimax.io/v1",
    "zai_official": "https://api.z.ai",
    "moonshot_official": "https://api.moonshot.ai/v1",
    "mistral_official": "https://api.mistral.ai/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "deepinfra": "https://api.deepinfra.com/v1/openai",
    "groq": "https://api.groq.com/openai/v1",
    "fireworks_ai": "https://api.fireworks.ai/inference/v1",
    "cerebras": "https://inference.cerebras.ai/v1",
}


@dataclass
class ResolvedEndpoint:
    provider: str
    model_id: str
    base_url: str
    api_key: str
    model_key: str


def api_key_for(settings: Any, provider: str) -> str:
    attr = PROVIDER_KEY_ATTR.get(provider)
    if not attr:
        return ""
    return (getattr(settings, attr, None) or "").strip()


def any_provider_key(settings: Any) -> bool:
    return any(api_key_for(settings, p) for p in PROVIDER_KEY_ATTR)


def chat_completions(
    *,
    base_url: str,
    api_key: str,
    model_id: str,
    messages: list[dict[str, str]],
    temperature: float,
    provider: str,
    timeout: float = 120.0,
) -> tuple[str, int, int, float | None]:
    """OpenAI-compatible chat/completions. Returns text, prompt_tokens, completion_tokens, cost."""
    url = base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if provider == "openrouter":
        headers["HTTP-Referer"] = "https://github.com/nandarishik/akara-jarvis"
        headers["X-Title"] = "JARVIS"
    payload = {
        "model": model_id,
        "messages": messages,
        "temperature": temperature,
    }
    with httpx.Client(timeout=timeout) as client:
        resp = client.post(url, headers=headers, json=payload)
        if resp.status_code in (429, 500, 502, 503, 504):
            raise httpx.HTTPStatusError(
                f"provider {provider} status {resp.status_code}",
                request=resp.request,
                response=resp,
            )
        resp.raise_for_status()
        data = resp.json()
    text = (data.get("choices") or [{}])[0].get("message", {}).get("content") or ""
    usage = data.get("usage") or {}
    prompt_tokens = int(usage.get("prompt_tokens") or 0)
    completion_tokens = int(usage.get("completion_tokens") or 0)
    cost = usage.get("cost")
    return text, prompt_tokens, completion_tokens, float(cost) if cost is not None else None
