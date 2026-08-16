# Model routing (Portfolio B)

**Source:** Model Research (2026-08-17), promoted to `config/`.

## Default

| Setting | Value |
|---|---|
| Portfolio | `B` (`MODEL_PORTFOLIO`) |
| Config dir | `config/` (`MODEL_CONFIG_DIR`) |
| Files | `model-registry.yaml`, `model-routing.yaml`, `provider-fallbacks.yaml` |

Dispatch is **by agent + risk**, not by `TIER0_MODEL` env slots (those are ignored).

## Keys

OpenRouter alone is enough to boot (every chain can fall back to it). Prefer official APIs when set:

| Env | Provider |
|---|---|
| `DEEPSEEK_API_KEY` | DeepSeek |
| `MINIMAX_API_KEY` | MiniMax |
| `ZAI_API_KEY` | Z.ai (GLM) |
| `MOONSHOT_API_KEY` | Moonshot (Kimi) |
| `MISTRAL_API_KEY` | Mistral (Devstral) |
| `OPENROUTER_API_KEY` | Aggregator fallback |
| `GROQ_API_KEY` / `DEEPINFRA_API_KEY` | Emergency failover |

## Failover

On HTTP 5xx / 429 / timeout, the router walks `config/provider-fallbacks.yaml` for that model family. Missing keys skip a hop. `llm_calls.source` stores the provider id used.

MiniMax outage is critical (seven coding agents). See playbooks in the fallbacks YAML.

## Spend

Active Portfolio B ? **$50–150/mo**. `DAILY_SPEND_CAP_USD` default in `.env.example` is 50. A $20/mo budget is Portfolio C slow pace only.

## Checklist before Phase 8 “fully functional”

- [ ] MiniMax Community License reviewed for commercial autonomous agents
- [ ] Bake-off subset from `Model Research/model-evaluation-plan.md` (Architect, Backend auth, Code Review plants)
- [ ] Z.ai p95 latency from your region acceptable for Code Review
