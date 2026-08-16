from __future__ import annotations

from uuid import UUID

import httpx

from jarvis.config import Settings
from jarvis.db import store

TIER_RATES_PER_MTOK = {0: 0.15, 1: 0.15, 2: 3.0, 3: 15.0}


class BudgetExceeded(Exception):
    pass


class ModelRouter:
    def __init__(self, settings: Settings, conn) -> None:
        self.settings = settings
        self.conn = conn
        self.models = {
            0: settings.tier0_model,
            1: settings.tier1_model,
            2: settings.tier2_model,
            3: settings.tier3_model,
        }

    def complete(
        self,
        *,
        tier: int,
        messages: list[dict[str, str]],
        task_id: UUID | None,
        agent: str | None,
        correlation_id: UUID | None,
        budget_remaining: int,
    ) -> tuple[str, int]:
        if not self.settings.openrouter_api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not set")
        model = self.models.get(tier, self.settings.tier0_model)
        headers = {
            "Authorization": f"Bearer {self.settings.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/nandarishik/akara-jarvis",
            "X-Title": "JARVIS Phase 1",
        }
        payload = {"model": model, "messages": messages, "temperature": 0.2}
        with httpx.Client(timeout=120.0) as client:
            resp = client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
        text = data["choices"][0]["message"]["content"] or ""
        usage = data.get("usage") or {}
        prompt_tokens = int(usage.get("prompt_tokens") or 0)
        completion_tokens = int(usage.get("completion_tokens") or 0)
        total = prompt_tokens + completion_tokens
        if total > budget_remaining:
            raise BudgetExceeded(
                f"call used {total} tokens; remaining budget {budget_remaining}"
            )
        usd = usage.get("cost")
        if usd is None:
            rate = TIER_RATES_PER_MTOK.get(tier, 0.15)
            usd = (prompt_tokens + completion_tokens) / 1_000_000 * rate
        spent = self.settings.daily_spend_cap_usd
        today = store.today_spend(self.conn)
        would_pause = (today + float(usd)) >= spent
        store.log_llm_call(
            self.conn,
            task_id=task_id,
            correlation_id=correlation_id,
            agent=agent,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            usd_estimate=float(usd),
            would_pause=would_pause,
        )
        return text, total
