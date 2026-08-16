-- JARVIS Phase 1 platform tables
CREATE TABLE IF NOT EXISTS intents (
  intent_id UUID PRIMARY KEY,
  correlation_id UUID NOT NULL,
  text TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS tasks (
  task_id UUID PRIMARY KEY,
  intent_id UUID NOT NULL REFERENCES intents (intent_id),
  correlation_id UUID NOT NULL,
  issue_key TEXT,
  agent TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN (
    'pending', 'in_progress', 'completed', 'failed', 'blocked'
  )),
  depends_on UUID[] NOT NULL DEFAULT '{}',
  input_artifacts TEXT[] NOT NULL DEFAULT '{}',
  output_artifacts TEXT[] NOT NULL DEFAULT '{}',
  model_tier INT NOT NULL DEFAULT 0,
  token_budget INT NOT NULL DEFAULT 8000,
  tokens_used INT NOT NULL DEFAULT 0,
  retry_count INT NOT NULL DEFAULT 0,
  max_retries INT NOT NULL DEFAULT 3,
  summary TEXT,
  blocking_issues JSONB NOT NULL DEFAULT '[]',
  needs_from JSONB NOT NULL DEFAULT '[]',
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS llm_calls (
  id BIGSERIAL PRIMARY KEY,
  timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
  task_id UUID,
  correlation_id UUID,
  agent TEXT,
  model TEXT NOT NULL,
  source TEXT NOT NULL DEFAULT 'openrouter',
  prompt_tokens INT NOT NULL DEFAULT 0,
  completion_tokens INT NOT NULL DEFAULT 0,
  usd_estimate NUMERIC(12, 6) NOT NULL DEFAULT 0,
  would_pause BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS spend_daily (
  day DATE PRIMARY KEY,
  usd_spent NUMERIC(12, 6) NOT NULL DEFAULT 0
);
