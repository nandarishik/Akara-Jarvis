# Phase 5 Constitution — Reliability

**Duration:** 1–2 days  
**Depends on:** Phase 4 Exit Gate  
**Unlocks:** Phase 6  
**Parent:** [`../SWE TEAM.MD`](../SWE%20TEAM.MD) · Index: [`PHASES.md`](PHASES.md)

After this phase, JARVIS is allowed to be left running. Before this phase, it is a demo that dies when you close a laptop lid.

---

## 1. Purpose

1. Prove crash recovery from LangGraph Postgres checkpoints  
2. Structured JSON logs with correlation IDs across orchestrator and workers  
3. Context package assembly that is complete without pgvector  
4. **First real project** through spec → QC quality gate (prod still human/Phase 7)  
5. Fix everything that run surfaces  

This is not "add Sentry." V1 observability is logs + health + platform dashboards + JARVIS task log.

---

## 2. Non-negotiables

1. Every JARVIS state transition is checkpointed: task created, assigned, completed, failed, pipeline advanced.
2. On restart, JARVIS **reconciles git** (commits/PRs that finished while it was dead) with graph state. Checkpoint-only without git reconcile is incomplete.
3. No infinite loops (already law). Reliability means timeouts: **default 30 minutes per task**, kill worker, mark failed, retry policy applies.
4. Logs are **JSON lines**: `timestamp`, `level`, `correlation_id`, `message`, `context` (task_id, agent, sha).
5. Correlation ID starts at the user intent and follows every agent, CI pointer, and worker log.
6. Context package is assembled **every** task. RAG waits for Phase 6. Always-on files follow index **C5** (include if present; block only if this task depends on a missing artifact).
7. The first real run is a **non-todo** product idea (still small). A second copy of the Phase 1 todo app does not count.
8. Observability V2 (Prometheus, Grafana, Loki, Jaeger, Sentry) is **forbidden** in this phase.
9. Task timeout must **fire** in a drill (Phase 1 only required it to be configured).

---

## 3. Crash recovery drill (mandatory)

**Procedure:**

1. Start a `jarvis build` that will take several minutes  
2. Kill JARVIS (process kill, not graceful) mid-agent  
3. Confirm Postgres still has last checkpoint  
4. Restart JARVIS  
5. Confirm: no duplicate destructive git operations; in-flight task resumes or is marked failed cleanly; completed git work is recognized  

**Pass:** operator can describe the recovered state in one paragraph. Write it in `docs/runbook/crash-recovery.md`.

---

## 4. Logging law

Every service JARVIS **is** (orchestrator, API, workers) emits structured JSON.

Minimum fields:

```json
{
  "timestamp": "ISO-8601",
  "level": "debug | info | warn | error",
  "correlation_id": "uuid",
  "task_id": "uuid | null",
  "agent": "string | null",
  "message": "string",
  "context": {}
}
```

No bare `print` as the production log path.

Health: JARVIS stack exposes `/healthz` (or documented equivalent) polled on an interval (doc: 60s). Implementation now. Fancy dependency graphs can wait.

---

## 5. Context package (V1 complete)

JARVIS builds, in order:

1. Role definition  
2. Project summary (from README + architecture docs)  
3. Task spec + acceptance criteria  
4. Relevant code — **without pgvector:** path/keyword selection from the task + always-on files  
5. Relevant artifacts  
6. Previous attempts on retry  

Always-on **when present** (index **C5**):

- `docs/api/contracts.yaml`
- `database/schema.sql`
- `docs/architecture/decisions.md`
- `docs/design/tokens.json`

If a **required** file is missing, the agent is `blocked` with `needs_from`, not hallucinating.

---

## 6. First real run protocol

Pick one intent that needs **frontend + backend + database** and at least one auth-sensitive path.

**Watch for (expected):**

- Agent timing / race on parallel FE/BE  
- Context too large  
- Wrong model tier  
- Flaky QA  
- Contract drift  

**Budget:** hours of seam-fixing after the run. That time is the phase, not an embarrassment.

**Record** in `docs/runbook/first-real-run.md`:

- Intent text  
- Task graph outcome  
- Tokens and estimated USD  
- Failures and retries  
- Dead letters  
- What we changed in prompts/code after  

---

## 7. Out of scope

- pgvector / embedding index (Phase 6)
- CLI/daemon UX polish (Phase 6) — a working `jarvis build` from Phase 1 is enough
- Prod approval UX (Phase 7)
- Operate-at-scale week (Phase 8)

---

## 8. Exit gate

- [ ] Kill-mid-pipeline drill passed and runbooked
- [ ] Git reconciliation on restart described and implemented
- [ ] JSON logs with correlation IDs from intent → worker
- [ ] Task timeout exists and **fires** in a drill
- [ ] Context package follows C5 (not "block the world if tokens.json is absent")
- [ ] First real (non-toy-repeat) project reached QA gate on QC
- [ ] Post-run fixes merged; known issues listed if not fixed (no silent holes)

---

## 9. Failure modes

| Symptom | Likely cause |
|---|---|
| Double PR / double commit on resume | No git reconcile / no idempotent worker start |
| Recovery to ancient state | Checkpointer URL pointed at empty DB |
| Unusable logs | Non-JSON stdout from workers not forwarded |
| Real run explodes context | Dumping whole repo; use package rules |
| "We'll fix flakes in Phase 8" | Flakes are Phase 4 regressions; fix now |

---

## 10. Time truth

The real-run debugging **is** Phase 5. Do not steal that time to start RAG or a dashboard theme.
