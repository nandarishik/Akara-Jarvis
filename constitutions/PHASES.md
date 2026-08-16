# JARVIS Phase Constitutions — Master Index

**Status:** Binding.  
**Parent law:** [`../SWE TEAM.MD`](../SWE%20TEAM.MD)  
**V1 target:** Fully functional by 16 September 2026 (Phases 1–8).  
**V2 target:** Full potential as specified in `SWE TEAM.MD` (Phases 9–14), **trigger-gated**, not calendar-gated.

This folder is the operating constitution for the build. `SWE TEAM.MD` is the product vision. These files are the law for *how* that vision is executed, phase by phase.

If a phase constitution conflicts with convenience, the constitution wins. If a phase constitution conflicts with `SWE TEAM.MD` design principles, `SWE TEAM.MD` wins — and the phase file must be amended, not silently ignored.

---

## How to use these files

1. Open **only the current phase** constitution before writing code.
2. **V1 (1–8):** do not start the next phase until that file's **Exit Gate** is green.
3. **V2 (9–14):** do not start until that file's **Trigger** is true. V2 phases are **not** a queue you burn down after Sept 16 for sport.
4. Every PR, agent prompt, and infra change in a phase must satisfy that phase's **Non-Negotiables**.
5. Out-of-scope work is not "extra credit." It is a constitutional violation.
6. When debugging, the phase file's **Failure Modes** section is the first checklist.
7. **Exit gates are binary.** A human initials the phase file (or a `docs/runbook/gates.md` line) with date. Unchecked boxes mean the phase is not done.
8. **Amendments:** change the phase file in git. Do not override a constitution in a chat. If `SWE TEAM.MD` §3 agent prose conflicts with §8 model-tier table, **§8 + this index win.**

---

## V1 — Fully functional (Phases 1–8)

| # | File | Name | Finishes |
|---|---|---|---|
| 1 | [PHASE-01-CORE.md](PHASE-01-CORE.md) | JARVIS Core | Orchestrator + worker + models + first proof of life |
| 2 | [PHASE-02-AGENT-TEAM.md](PHASE-02-AGENT-TEAM.md) | Agent Team | 13 roles (JARVIS + 12 agents), review gate, budgets, handoffs |
| 3 | [PHASE-03-PIPELINE.md](PHASE-03-PIPELINE.md) | Pipeline & Environments | CI/CD, DEV / QC / prod promotion |
| 4 | [PHASE-04-QUALITY-GATES.md](PHASE-04-QUALITY-GATES.md) | Quality Gates | QA, Security, autonomous repair loop |
| 5 | [PHASE-05-RELIABILITY.md](PHASE-05-RELIABILITY.md) | Reliability | Crash recovery, logs, first real run |
| 6 | [PHASE-06-INTELLIGENCE-CONTROL.md](PHASE-06-INTELLIGENCE-CONTROL.md) | Intelligence & Control | RAG, anti-slop, CLI/daemon/dashboard |
| 7 | [PHASE-07-PRODUCTION-DISCIPLINE.md](PHASE-07-PRODUCTION-DISCIPLINE.md) | Production Discipline | Migrations, rollback, hardening, human release |
| 8 | [PHASE-08-OPERATE.md](PHASE-08-OPERATE.md) | Operate | Spend, circuit breakers, boring full-loop operation |

**Fully functional** = Phases 1–8 complete.

**Note:** `SWE TEAM.MD` §15 listed codebase RAG as V2. It was **pulled forward into Phase 6** so Sept 16 agents can retrieve code. Do not rebuild RAG in V2 unless Phase 9's RAG-quality clause applies.

---

## V2 — Full potential (Phases 9–14)

These are the rest of the vision: self-hosted inference, canaries, observability that pages JARVIS, Temporal, load/cache, sovereign CI, and earned auto-release.

| # | File | Name | What "full potential" adds |
|---|---|---|---|
| 9 | [PHASE-09-SELF-HOSTED-INFERENCE.md](PHASE-09-SELF-HOSTED-INFERENCE.md) | Self-hosted inference | Ollama/vLLM Tier 0; optional local embeddings |
| 10 | [PHASE-10-PROGRESSIVE-DELIVERY.md](PHASE-10-PROGRESSIVE-DELIVERY.md) | Progressive delivery | Unleash, 5→25→100% canary, auto app rollback (never DB) |
| 11 | [PHASE-11-OBSERVABILITY.md](PHASE-11-OBSERVABILITY.md) | Observability & incidents | OTel, Prometheus, Grafana, Loki, Jaeger, Sentry; JARVIS investigates |
| 12 | [PHASE-12-TEMPORAL.md](PHASE-12-TEMPORAL.md) | Durable execution | Temporal for hour/day workflows |
| 13 | [PHASE-13-PERFORMANCE-SCALE.md](PHASE-13-PERFORMANCE-SCALE.md) | Performance & scale | k6 vs real baselines; Redis when DB is proven hot |
| 14 | [PHASE-14-SOVEREIGN-OPS.md](PHASE-14-SOVEREIGN-OPS.md) | Sovereign ops & auto-release | Forgejo+Woodpecker if required; low-risk auto-prod after 20 releases |

### Triggers (copy of `SWE TEAM.MD` §15 — law)

| Phase | Start when |
|---|---|
| 9 | OpenRouter rate limits (or hard $0 Tier 0), or embedding cost/latency forces local |
| 10 Unleash | You need canaries / gradual rollout (V1 all-or-nothing is not enough) |
| 10 Auto-rollback | Deploy frequency makes manual rollback too slow |
| 11 Grafana/Prom/Loki/Jaeger | Real-time dashboards or automated alerting required |
| 11 Sentry | Prod runs continuously with real users |
| 12 Temporal | Workflows routinely last hours/days; LangGraph checkpoints are not enough |
| 13 k6 | You have traffic **baselines** |
| 13 Redis | Queries are a **measured** bottleneck |
| 14 Auto-release | **20+** successful production releases |
| 14 Forgejo + Woodpecker | Self-hosted CI is a **hard** requirement |

V2 phases **may run in parallel** if multiple triggers are true. They must **not** run before Phase 8. Auto-release (14) should not outrun auto-rollback (10) if you ship many times per day.

---

## Canonical law (resolves conflicts across files)

These rules exist because the phase drafts disagreed with each other or with `SWE TEAM.MD` internals. They are binding.

### C1 — Two roots (platform ≠ product)

| Root | What it is | Who writes it |
|---|---|---|
| **Platform** | JARVIS itself: orchestrator, prompts, constitutions, worker images, CLI | You + JARVIS-platform PRs |
| **Product** | Each `projects/{name}/` (or equivalent) matching the artifact tree | Agents, scoped |

Do not dump LangGraph into `frontend/`. Do not treat `SWE TEAM.MD` as an app README. Phase 1 scaffolds **both**: platform runnable, and the product tree **inside** a project workspace.

### C2 — Thirteen roles, not fourteen

JARVIS + Product, Architect, Design, Frontend, Backend, AI/ML, Database, Code Review, QA, Security, DevOps, Documentation. **OpenHands (or fallback) is the engine, not a 14th agent.** Older notes saying “14 prompts” were a miscount.

### C3 — Model tier integers (authoritative)

`SWE TEAM.MD` §3 sometimes calls Opus “Tier 1” and Composer “Tier 3”. **Ignore that.** Use §8:

| Tier | Meaning | Examples |
|---|---|---|
| **0** | Free/grunt | Composer 2.5 class, local Ollama (Phase 9) |
| **1** | Cheap | Haiku / GPT-4o-mini class |
| **2** | Mid | Sonnet / JARVIS / Code Review default |
| **3** | Premium | Opus / o3 class — Architect always; Product if ambiguous |

Every LLM call goes through the **model router**. V1 backend is OpenRouter. Phase 9 may add local for Tier 0. Agents never call a vendor SDK with a hardcoded model.

### C4 — Retries are per issue, not per mood

`max_retries = 3` applies to the same **issue_key** (task id + fingerprint of test name / error class / file hunk). A new distinct bug gets its own counter. After 3: dead letter. No silent fourth try.

### C5 — Always-on context files

`contracts.yaml`, `schema.sql`, ADRs, `tokens.json` are included **when they exist**. Missing a file the **current task depends on** → `blocked` + `needs_from`. Missing `tokens.json` during Product-only work is not a block.

### C6 — Secret scan default

**Gitleaks** is the default. TruffleHog is an allowed substitute, not both required.

### C7 — Health watch

Post-deploy: poll `/healthz` every **10s for 5 minutes**. **3 consecutive** failures = unhealthy (V1: notify; Phase 10: auto-rollback app tiers only).

### C8 — Successful production release (counts toward Phase 14’s 20)

A row in the deployment table: git tag, SHA, prod URLs, migration ids if any, **5-minute health pass**, Documentation Agent ran (or explicitly skipped with reason). Preview/DEV/QC deploys do not count.

---

## Global laws (apply in every phase, V1 and V2)

Copied from `SWE TEAM.MD` Design Principles. These cannot be waived by a phase.

1. **Open source or don't use it** — exceptions: Vercel, Railway, Supabase, OpenRouter.
2. **Cheap models do grunt work** — Composer 2.5 / Tier 0 for implementation from detailed plans.
3. **Plans before code** — no engineering until Product acceptance criteria and Architect contracts exist (Phase 1 may use a stub Product/Architect for proof of life only).
4. **Agents don't trust themselves** — author ≠ reviewer; QA hits the running app; Security runs tools.
5. **Fail fast, fix, escalate** — max 3 retries, then human. No infinite loops. No silent failures.
6. **Forward-only data, immutable deploys.** Auto-rollback never rolls the database backward.
7. **No AI-slop UI. Ever.**

---

## Sequence

**V1 (strict):**

```
01 Core → 02 Agents → 03 Pipeline → 04 Quality
                                      ↓
08 Operate ← 07 Prod discipline ← 06 Intelligence ← 05 Reliability
```

**V2 (trigger fan-out after 08):**

```
                    ┌→ 09 Inference
                    ├→ 10 Progressive delivery
08 Operate ─────────┼→ 11 Observability + autonomous incidents
                    ├→ 12 Temporal
                    ├→ 13 k6 / Redis
                    └→ 14 Auto-release / sovereign CI
                         (14 auto-release needs 20 prod ships;
                          high-frequency auto-prod needs 10 rollback)
```

---

## Definition of "fully functional" (16 September — V1)

You can say `jarvis build "<product idea>"` and JARVIS will:

1. Produce PRD, API contracts, design specs as git artifacts
2. Implement frontend, backend, database (and AI features if specified)
3. Gate every PR through Code Review
4. Run CI on DEV, promote to QC, run QA + Security
5. Retry failures up to 3 times, then escalate with full context
6. Present a release summary; you approve production
7. Deploy, health-check, document, and remain recoverable from crash

---

## Definition of "full potential" (V2 — after triggers)

V1, plus as each phase's trigger is met:

1. Tier 0 can run on your metal with OpenRouter failover (9)
2. Features can ship dark and canary; bad app deploys auto-roll back; DB stays forward-only (10)
3. Metrics/logs/traces/errors page JARVIS; it files a fix through the pipeline (11)
4. Hour- and day-long workflows survive restarts (12)
5. Load tests match real traffic; cache exists only where measured (13)
6. Low-risk changes auto-ship after 20 proven releases; CI can leave GitHub if sovereignty is required (14)

High-risk (schema, auth, payments, deletion) **never** auto-ships without a human. That remains true at full potential.

---

## Audit log

| Date | What |
|---|---|
| 2026-08-16 | Initial eight V1 constitutions |
| 2026-08-16 | V2 phases 9–14 added |
| 2026-08-16 | Consistency pass: 13 roles, canonical tiers, two-root law, router vs OpenRouter, retry identity, healthz/smoke, always-on files, Gitleaks default, release counting |
