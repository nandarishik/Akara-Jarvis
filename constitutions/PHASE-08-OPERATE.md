# Phase 8 Constitution — Operate

**Duration:** 3–4 days  
**Depends on:** Phase 7 Exit Gate  
**Unlocks:** Fully functional (16 September target). V2 constitutions [PHASE-09](PHASE-09-SELF-HOSTED-INFERENCE.md)–[PHASE-14](PHASE-14-SOVEREIGN-OPS.md) unlock **only when their triggers fire.**  
**Parent:** [`../SWE TEAM.MD`](../SWE%20TEAM.MD) · Index: [`PHASES.md`](PHASES.md)

This phase makes the lifecycle **boring**. Fully functional is not a single green demo. It is several real intents, spend control that actually pauses work, and escalations a human can act on.

---

## 1. Purpose

Run JARVIS as an operator would:

- Daily/monthly spend caps that pause non-critical work  
- Agent-level and task-level circuit breakers proven in anger (or staged)  
- Post-deploy health watch (10s / 5 min) with notification to JARVIS  
- Escalation UX that dumps dead-letter context, not a shrug  
- **Multiple** distinct `jarvis build` runs until failure modes are known  

When this phase exits, you can tell JARVIS to build something **without babysitting the graph**, and you only return for approvals and dead letters.

---

## 2. Non-negotiables

1. If 80% of monthly LLM budget is consumed before the 20th, **non-critical tasks pause** and you are notified. Critical = production fixes only.
2. Daily cap ≈ monthly/30. Same pause rule.
3. Agent breaker: 5 consecutive failures → that agent pauses, human alert. Do not keep burning tokens on a broken prompt.
4. Task breaker: 3 failures **per issue_key** → dead letter with full context. Always.
5. No silent failures. Every terminal state is `completed`, `failed` (with reason), or `blocked` (with `needs_from`) or dead-lettered.
6. Production still requires **you** (Phase 7 law). Phase 8 does not sneak in auto-release.
7. Do not "finish" this phase by writing more architecture. Finish it by **running builds**.
8. V2 platforms stay **off** unless a trigger in [`PHASES.md`](PHASES.md) / `SWE TEAM.MD` §15 is **already true**. Curiosity is not a trigger. When a trigger fires, open that phase's constitution — do not invent a side project.

---

## 3. Operate loop (the lifecycle, now live)

```
You: "Build X"
  → Product (Tier 2)
  → Architect (Tier 3) ∥ Design (Tier 1)
  → Task graph
  → Frontend ∥ Backend ∥ AI/ML ∥ Database (tiered models)
  → Code Review (Tier 2)
  → develop → DEV CI
  → QC
  → QA ∥ Security
  → FAIL → responsible agent → review → DEV → QC (max 3)
  → Release gate + your approval
  → Production
  → Health + smoke + Documentation Agent
  → JARVIS waits
```

Phase 8's job is to run this **enough times** that the seams are dull.

---

## 4. Spend & routing truth

Production routing **must** match `config/model-routing.yaml` (Portfolio B default), not a stale markdown table in `SWE TEAM.MD`.

| Agent | Primary (B) |
|---|---|
| JARVIS / Security / Docs | DeepSeek V4 Flash |
| Product / Architect | DeepSeek V4 Pro |
| Design / FE / BE / DB / QA / DevOps | MiniMax M3 |
| AI/ML | Kimi K2.6 |
| Code Review | GLM-5.2 (cross-family; high-risk → Kimi K3) |

**Spend realism (Model Research):** active development on Portfolio B is about **$50–150/mo** (5–15 features/week). A **$20/mo** LLM budget is only plausible on Portfolio C at slow pace. Caps in `.env` must reflect the chosen portfolio.

Prompt cache on. Artifact/context cache on. Dedup retrieval on.

**Bake-off Go/No-Go:** before claiming Phase 8 “fully functional,” run (or schedule) the harness in `Model Research/model-evaluation-plan.md` for Architect, Backend auth, and Code Review planted defects. MiniMax Community License must be on the legal checklist (`docs/runbook/models.md`).

Self-hosted Ollama/vLLM only via [PHASE-09](PHASE-09-SELF-HOSTED-INFERENCE.md) when **its trigger** is true — not "this week felt slow." Hosted Portfolio B usually removes the **cost** trigger for Phase 9.

---

## 5. Post-deploy watch (V1)

For 5 minutes after prod: health every 10s.

On **3 consecutive** health failures (C7): **notify** with logs + SHA + release summary. V1: human/JARVIS investigate; optional app-tier rollback script from Phase 7. **Never** auto-rollback DB.

JARVIS task log in Postgres remains the system of record for agent activity.

V1 observability remains:

- Structured JSON logs  
- Health polling  
- Vercel/Railway dashboards  
- GitHub Actions summaries  
- JARVIS task log + spend log  

---

## 6. Escalation UX (minimum)

When a dead letter is created, the human sees **in one place** (dashboard or CLI):

- Intent  
- Spec pointers  
- Attempts (n/3)  
- Error output  
- Diff or file list generated  
- Suggested next instruction box (`jarvis resume --task <id> --note "..."`)

If the human cannot resume with extra instruction, the DLQ is incomplete.

---

## 7. The operate week (definition of done for "several builds")

Run **at least five** intents, of which:

- At least **3** are different product domains (not five CRUD clones with renamed nouns)
- At least **1** includes an AI/ML feature path (`ai/` prompts versioned + eval stub)
- At least **1** includes a schema change that goes through migration lock / dry-run
- At least **1** is forced into retry (natural or staged) and either recovers or dead-letters correctly
- At least **1** reaches **human prod approval** (real prod or dedicated prod project)

Record each run: tokens, USD, wall time, retries, DLQs, whether UI slop gate fired.

---

## 8. What "fully functional" means at Exit Gate

From `PHASES.md`, all must be true:

1. PRD, contracts, design as git artifacts  
2. FE/BE/DB (+ AI if asked) implemented by workers  
3. Code Review gates PRs  
4. DEV CI → QC → QA + Security  
5. Retry ≤ 3 then escalate with context  
6. Release summary; human prod approval  
7. Deploy, health-check, docs, crash-recoverable  

Plus: spend pause works; dashboard/CLI is how you live in the system.

---

## 9. Out of scope (still)

These have their own V2 constitutions. Writing them "so we're ahead" **violates** this constitution.

| Item | Constitution | Trigger |
|---|---|---|
| Ollama / vLLM | [PHASE-09](PHASE-09-SELF-HOSTED-INFERENCE.md) | Rate limits or hard $0 Tier 0 |
| Unleash / auto app-rollback | [PHASE-10](PHASE-10-PROGRESSIVE-DELIVERY.md) | Canaries needed / rollback too slow by hand |
| Grafana / Prom / Loki / Jaeger / Sentry | [PHASE-11](PHASE-11-OBSERVABILITY.md) | Real dashboards/alerts; continuous users |
| Temporal | [PHASE-12](PHASE-12-TEMPORAL.md) | Hour/day workflows; checkpoints not enough |
| k6 / Redis | [PHASE-13](PHASE-13-PERFORMANCE-SCALE.md) | Baselines / measured DB bottleneck |
| Auto-release / Forgejo | [PHASE-14](PHASE-14-SOVEREIGN-OPS.md) | 20+ prod releases / self-host CI is hard requirement |

---

## 10. Exit gate (16 September)

- [ ] Five-run operate log exists and is honest
- [ ] Spend pause demonstrated (can be a lowered cap in a drill)
- [ ] Agent pause after 5 consecutive failures demonstrated
- [ ] Dead letter resume path works with human note
- [ ] Post-deploy 5-minute watch runs
- [ ] Lifecycle diagram in `SWE TEAM.MD` matches the running system (if not, **change the system or amend the doc** — do not live with drift)
- [ ] Known limitations listed (what "build anything" still cannot do: native mobile, giant monorepo migrations, etc.)
- [ ] At least one C8 successful prod release is in the deployment table (the 20-count starts here)
- [ ] Bake-off Go/No-Go recorded (or explicitly deferred with date) for Architect / Backend auth / Code Review
- [ ] No V2 infra merged "just in case"

---

## 11. Failure modes

| Symptom | Likely cause |
|---|---|
| One beautiful demo, four unrun ideas | You skipped operate; stay in this phase |
| Spend graph decorative | Pause not wired to scheduler |
| Always Tier 3 | Routing table not enforced |
| Human still SSHs to fix workers | Control plane regression |
| Auto-merge to prod "just this once" | Constitutional breach; revert |

---

## 12. Time truth

Calendar time here is **runtime**, not Cursor time. Leave the system on. Watch it fail. Fix seams. That is the work. After Exit Gate, you are fully functional. You are not done forever — you are done with the law required for 16 September.
