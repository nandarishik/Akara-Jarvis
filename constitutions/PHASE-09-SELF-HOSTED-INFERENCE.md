# Phase 9 Constitution — Self-Hosted Inference (V2)

**Track:** Full potential (V2+)  
**Depends on:** Phase 8 Exit Gate  
**Unlocks:** cheaper/unlimited Tier 0; not a prerequisite for Phases 10–14 unless OpenRouter is down  
**Parent:** [`../SWE TEAM.MD`](../SWE%20TEAM.MD) §8, §14, §15 · Index: [`PHASES.md`](PHASES.md)

---

## 0. Trigger (start only if true)

**Start this phase when at least one is true:**

1. OpenRouter free/cheap-tier **rate limits** block JARVIS on a normal operate week, or  
2. You have a **hard requirement** for zero-cost Tier 0 (electricity only), or  
3. Embedding calls are a measurable cost/latency problem and Sentence Transformers on-box is cheaper.

**Do not start** because GPUs are interesting.

---

## 1. Purpose

Run **Tier 0 grunt work** on [Ollama](https://github.com/ollama/ollama) (MIT) and/or [vLLM](https://github.com/vllm-project/vllm) (Apache 2.0). Keep OpenRouter for Tier 1–3 unless you later self-host those too (not required).

Optional: self-host embeddings via [Sentence Transformers](https://github.com/UKPLab/sentence-transformers) (Apache 2.0). pgvector stays the store (Phase 6). This phase does **not** rebuild RAG; it can **swap the embedder**.

---

## 2. Non-negotiables

1. Open source inference stacks only (Ollama / vLLM). No new proprietary model-host lock-in.
2. JARVIS **model router** stays the single door. Agents never hardcode `localhost:11434`. They ask for a tier; the router picks OpenRouter vs local.
3. If local is down or slow past SLA, **fail over to OpenRouter** for that task. No hung pipeline because Ollama restarted.
4. Token/cost logs still record model id, source (`openrouter | ollama | vllm`), tokens, and USD (`$0` for local; still log token counts).
5. Local models are for **Tier 0** (index **C3**) unless quality evals prove a specific local model matches a higher tier for a named job. Do not silently demote Architect from Tier 3 to a 7B.
6. GPU/RAM ops are documented in `docs/runbook/inference.md` (start, stop, disk, models pulled, VRAM).
7. Prompt caching / budgets / daily pause still apply. Local is not an excuse for infinite loops.

---

## 3. In scope

| Work | Law |
|---|---|
| Ollama and/or vLLM in compose/systemd | Pinned model tags, not `latest` |
| Router fallback chain | Tier 0: local → OpenRouter cheap → fail |
| Health | Inference health endpoint; JARVIS marks source `degraded` |
| Embedding swap | Same chunking/index as Phase 6; re-embed policy documented |
| Eval harness | Golden tasks: generate a function, a test, a Dockerfile — local vs Composer-class |

---

## 4. Out of scope

- Training or fine-tuning foundation models
- Replacing Architect / Code Review with local-only (unless evals pass — default **no**)
- Temporal, Grafana, Unleash, Forgejo
- Rebuilding pgvector from scratch

**RAG note:** Codebase RAG shipped in Phase 6 (ahead of the original V2 trigger in `SWE TEAM.MD` §15). Quality work (re-rank, evals, chunk tuning) may happen here **if** wrong-code-from-missing-context is the live failure mode.

---

## 5. Exit gate

- [ ] Trigger written down (which of the three fired)
- [ ] Tier 0 can complete a Backend grunt task entirely on local
- [ ] Kill local inference mid-task → OpenRouter failover → task completes or fails cleanly
- [ ] Spend log shows `source=ollama|vllm` with $0
- [ ] `docs/runbook/inference.md` exists
- [ ] Architect still uses Tier 3 remote unless an ADR + eval says otherwise

---

## 6. Failure modes

| Symptom | Likely cause |
|---|---|
| Garbage implementations | Local model too weak; keep Tier 0 fallback to Composer-class |
| VRAM thrash | Too many models loaded; pin one grunt model |
| Router bypass | Worker env pointing at Ollama ad hoc |
| Re-embed storm | Full re-index on every boot; incremental only |
