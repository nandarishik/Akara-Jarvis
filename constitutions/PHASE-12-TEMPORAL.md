# Phase 12 Constitution — Durable Execution (V2)

**Track:** Full potential (V2+)  
**Depends on:** Phase 8 Exit Gate  
**Unlocks:** workflows that last hours/days without LangGraph checkpointer gymnastics  
**Parent:** [`../SWE TEAM.MD`](../SWE%20TEAM.MD) §14 Temporal, §15 · Index: [`PHASES.md`](PHASES.md)

---

## 0. Trigger (start only if true)

Workflows **routinely span hours or days** and LangGraph Postgres checkpointing is **not robust enough** (lost timers, stuck human-wait, deploy kills in-flight canaries, multi-day migrate-and-observe).

**Do not start** because Temporal is fashionable. Significant infrastructure overhead is the reason the spec waits.

---

## 1. Purpose

Adopt [Temporal](https://github.com/temporalio/temporal) (MIT) for **long-running JARVIS workflows**, not for "every function call."

LangGraph remains the **agent reasoning / task DAG** for short steps. Temporal owns:

- Human approval waits (hours)  
- Canary ramps (Phase 10) that sleep between 5% / 25% / 100%  
- Post-deploy 5-minute health loops and retries across process restarts  
- Multi-day "watch then drop old column" (still a **forward** migration later — Temporal only **schedules** the reminder/task)  
- Incident investigate that must survive JARVIS restarts better than ad-hoc cron  

---

## 2. Non-negotiables

1. Temporal is self-hosted (or OSS-compatible). No "Temporal Cloud only" as the constitution without an ADR that still avoids vendor lock-in of **workflow definitions**.
2. **Do not** rewrite all 14 agents as Temporal activities on day one. Port **one** workflow (recommended: release gate wait + post-deploy watch).
3. Agents still communicate via **git artifacts**. Temporal carries **signals and state**, not source code blobs as the source of truth.
4. Idempotent activities: create PR, deploy, rollback, send alert — safe to retry.
5. Killing Temporal workers must not corrupt git or double-apply migrations. Migration apply stays a single gated activity with a lock.
6. Secrets not in workflow histories. History is not a log of tokens/PII.
7. Max 3 repair attempts still encoded in the workflow, not an infinite retry policy.
8. Postgres checkpointer can remain for LangGraph subgraphs. Dual state must be **reconciled** (workflow id on the task row).

---

## 3. In scope

- Temporal cluster (Postgres/Cassandra per Temporal docs — prefer Postgres to stay in-family)
- Workers for JARVIS orchestrator activities
- Workflow IDs linked to `task_id` / release SHA
- Runbook: `docs/runbook/temporal.md` (what happens if cluster dies; how to reset a workflow)

---

## 4. Out of scope

- Replacing OpenHands  
- Replacing Code Review  
- Using Temporal as a message bus for Product → Architect files  
- k6, Redis, Forgejo unless their own phases/triggers  

---

## 5. Exit gate

- [ ] Trigger recorded with an example of a workflow that actually spanned hours  
- [ ] One production-shaped workflow (approval wait **or** canary ramp **or** health watch) survives JARVIS + worker restart  
- [ ] Duplicate activity (deploy/rollback) cannot double-apply  
- [ ] Task row stores `temporal_workflow_id`  
- [ ] 3-fail still dead-letters  
- [ ] Runbook includes "Temporal is down, how do we ship" (manual Phase 7 path)

---

## 6. Failure modes

| Symptom | Likely cause |
|---|---|
| Two sources of truth | Graph says completed, workflow still running — missing reconcile |
| History size explosion | Logging full diffs/prompts into activity results |
| Migration applied twice | Activity not idempotent / lock missing |
| Everything is a workflow | Scope creep; push short tasks back to LangGraph |
