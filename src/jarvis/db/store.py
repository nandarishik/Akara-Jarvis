from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any
from uuid import UUID

import psycopg
from psycopg.types.json import Json

SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def connect(database_url: str) -> psycopg.Connection:
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is empty. Copy the Postgres URI from Supabase → Settings → Database."
        )
    url = database_url
    if "sslmode" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}sslmode=require"
    return psycopg.connect(url)


def apply_schema(conn: psycopg.Connection) -> None:
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.execute(sql)
    conn.commit()


def insert_intent(conn: psycopg.Connection, intent_id: UUID, correlation_id: UUID, text: str) -> None:
    conn.execute(
        "INSERT INTO intents (intent_id, correlation_id, text) VALUES (%s, %s, %s)",
        (intent_id, correlation_id, text),
    )
    conn.commit()


def upsert_task(conn: psycopg.Connection, row: dict[str, Any]) -> None:
    conn.execute(
        """
        INSERT INTO tasks (
          task_id, intent_id, correlation_id, issue_key, agent, status,
          depends_on, input_artifacts, output_artifacts, model_tier,
          token_budget, tokens_used, retry_count, max_retries, summary,
          blocking_issues, needs_from, updated_at
        ) VALUES (
          %(task_id)s, %(intent_id)s, %(correlation_id)s, %(issue_key)s, %(agent)s, %(status)s,
          %(depends_on)s, %(input_artifacts)s, %(output_artifacts)s, %(model_tier)s,
          %(token_budget)s, %(tokens_used)s, %(retry_count)s, %(max_retries)s, %(summary)s,
          %(blocking_issues)s, %(needs_from)s, now()
        )
        ON CONFLICT (task_id) DO UPDATE SET
          issue_key = EXCLUDED.issue_key,
          status = EXCLUDED.status,
          input_artifacts = EXCLUDED.input_artifacts,
          output_artifacts = EXCLUDED.output_artifacts,
          tokens_used = EXCLUDED.tokens_used,
          retry_count = EXCLUDED.retry_count,
          summary = EXCLUDED.summary,
          blocking_issues = EXCLUDED.blocking_issues,
          needs_from = EXCLUDED.needs_from,
          updated_at = now()
        """,
        {
            **row,
            "blocking_issues": Json(row.get("blocking_issues") or []),
            "needs_from": Json(row.get("needs_from") or []),
        },
    )
    conn.commit()


def log_llm_call(
    conn: psycopg.Connection,
    *,
    task_id: UUID | None,
    correlation_id: UUID | None,
    agent: str | None,
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    usd_estimate: float,
    would_pause: bool,
) -> None:
    conn.execute(
        """
        INSERT INTO llm_calls (
          timestamp, task_id, correlation_id, agent, model, source,
          prompt_tokens, completion_tokens, usd_estimate, would_pause
        ) VALUES (%s, %s, %s, %s, %s, 'openrouter', %s, %s, %s, %s)
        """,
        (
            datetime.now(timezone.utc),
            task_id,
            correlation_id,
            agent,
            model,
            prompt_tokens,
            completion_tokens,
            Decimal(str(round(usd_estimate, 6))),
            would_pause,
        ),
    )
    today = date.today()
    conn.execute(
        """
        INSERT INTO spend_daily (day, usd_spent) VALUES (%s, %s)
        ON CONFLICT (day) DO UPDATE SET usd_spent = spend_daily.usd_spent + EXCLUDED.usd_spent
        """,
        (today, Decimal(str(round(usd_estimate, 6)))),
    )
    conn.commit()


def today_spend(conn: psycopg.Connection) -> float:
    row = conn.execute(
        "SELECT usd_spent FROM spend_daily WHERE day = %s", (date.today(),)
    ).fetchone()
    if not row:
        return 0.0
    return float(row[0])
