# Phase 1 Constitution — JARVIS Core

**Duration:** 3–4 days  
**Depends on:** nothing  
**Unlocks:** Phase 2  
**Parent:** [`../SWE TEAM.MD`](../SWE%20TEAM.MD) · Index: [`PHASES.md`](PHASES.md)

This is the hardest phase. It is integration-heavy, not code-heavy. The constitution exists so we ship a living loop instead of a pile of unconnected libraries.

---

## 1. Purpose

Stand up the spine:

**You → JARVIS (LangGraph + Postgres) → one execution worker → git artifacts / PR**

If this loop does not run on a real machine, no later phase matters.

---

## 2. Non-negotiables

1. JARVIS does **not** write product code. It orchestrates.
2. Task state is a **DAG** persisted in PostgreSQL via LangGraph's checkpointer. Memory-only graphs are illegal.
3. Coding work happens through an **execution worker** (OpenHands preferred) with filesystem scope, not by pasting code snippets into chat.
4. Agents communicate through **git artifacts**, not chat between agents.
5. Every LLM call goes through the **model router** (V1: multi-provider hosted; OpenRouter as aggregator fallback). Record model, **source = provider id**, tokens, cost. Agents do not call vendor APIs directly. Phase 9 may add a local backend; this bullet does not forbid that.
6. Every task has a **token budget**. Exhaustion requires an explicit JARVIS decision, not silent overrun.
7. Worker filesystem is scoped to the **product** workspace (`projects/{name}/` or documented root). JARVIS is not a general Windows administrator.
8. Kill switch: stopping the JARVIS process / compose stack stops workers. No orphan containers as the happy path.
9. Hard **task timeout** default 30 minutes: kill worker, `failed`, retry policy (index **C4**) applies.
10. Platform and product are separate roots (index **C1**). Phase 1 must run the platform and write into a product tree.

---

## 3. In scope

| Work | Constitutional requirement |
|---|---|
| LangGraph orchestrator | Task graph, status machine (`pending \| in_progress \| completed \| failed \| blocked`), dependency resolution |
| PostgreSQL checkpointer | Every state transition saved. Restart resumes from last checkpoint |
| OpenHands (or documented fallback runner) | Docker worker, workspace mount, process lifecycle owned by JARVIS |
| Model router | Agent map from `config/model-routing.yaml` (Portfolio B); provider chains in `config/provider-fallbacks.yaml`; log every call with provider `source` |
| Two-root scaffold | Platform package + product tree in §5 |
| Proof of life | `jarvis build "<X>"` → JARVIS assigns **one** agent → code or spec lands in a branch/PR |

---

## 4. Out of scope (violations if built now)

- All 14 production-quality agent prompts (Phase 2)
- Code Review as a real gate (Phase 2) — a stub node that always-approves is allowed only for proof of life and **must be labeled STUB**
- GitHub Actions, Vercel, Railway, QC, production (Phase 3)
- Playwright, Semgrep, Trivy, ZAP (Phase 4)
- RAG / pgvector (Phase 6)
- Dashboard polish, Temporal, Grafana, Ollama

**OpenHands fallback (allowed):** If OpenHands on Windows burns more than two days, a thin runner (shell + file edit + git) is constitutional **provided** it is behind the same worker interface OpenHands would use. Do not leak runner details into every agent node.

---

## 5. Artifact law (repo shape)

This tree is the handshake. Do not invent a parallel document store.

**Platform** (this workspace, e.g. `jarvis/`): orchestrator, prompts, constitutions, compose, CLI.

**Product** (each build):

```
projects/{name}/
├── docs/
│   ├── product/
│   ├── architecture/
│   ├── api/
│   ├── design/
│   ├── security/
│   └── runbook/
├── frontend/
├── backend/
├── ai/
├── database/
│   ├── migrations/
│   ├── seeds/
│   └── schema.sql
├── infra/
│   ├── docker/
│   └── monitoring/
├── tests/e2e/
└── .github/workflows/
```

Phase 1 may only *create* this skeleton and write into one agent's folder. Empty dirs are required, not optional.

---

## 6. Task node contract

Every task JARVIS schedules **must** be this shape (fields may be added later, none may be removed):

```json
{
  "task_id": "uuid",
  "intent_id": "uuid",
  "correlation_id": "uuid",
  "issue_key": "string | null",
  "agent": "frontend | backend | product | architect | ...",
  "status": "pending | in_progress | completed | failed | blocked",
  "depends_on": [],
  "input_artifacts": [],
  "output_artifacts": [],
  "model_tier": 0,
  "token_budget": 8000,
  "tokens_used": 0,
  "retry_count": 0,
  "max_retries": 3
}
```

`intent_id` and `correlation_id` are shared by all tasks of one `jarvis build`. `issue_key` is set on retries (index **C4**).

Agent completion **must** return:

```json
{
  "agent": "string",
  "task_id": "uuid",
  "status": "completed | failed | blocked",
  "summary": "string",
  "artifacts_created": [],
  "artifacts_modified": [],
  "tokens_used": 0,
  "blocking_issues": [],
  "needs_from": []
}
```

If `blocked`, `needs_from` is mandatory (`agent`, `artifact`, `reason`).

---

## 7. Model routing (minimum viable)

Dispatch by **agent role** (not env `TIER*_MODEL` slots). Phase 1 proof uses the **backend** agent entry from Portfolio B:

| Agent (Phase 1) | Primary | Fallback path |
|---|---|---|
| Backend (OpenHands / fallback worker) | MiniMax M3 | OpenRouter MiniMax → Kimi / V4 Pro escalate |
| JARVIS routing (when used) | DeepSeek V4 Flash | OpenRouter / GPT-OSS-120B |

OpenHands model string comes from `openhands_settings` in `config/model-routing.yaml`.

Log: timestamp, task_id, correlation_id, agent, model, source (**provider id**, e.g. `minimax_official` / `openrouter`), prompt tokens, completion tokens, USD estimate.

Daily spend tracking can be a table + log line. Pause logic can be stubbed if it **records** that it would have paused.

---

## 8. Worker law

```
JARVIS assigns task
  → worker spins up (Docker)
  → branch: feature/TASK-{id}-short-description
  → agent writes files
  → lint/type/unit if they exist; if they don't, skip is allowed in Phase 1 only
  → open PR against develop (or local equivalent)
```

**Filesystem scopes** (product root; enforce in the runner):

| Agent | Write scope |
|---|---|
| Product | `docs/product/` |
| Architect | `docs/architecture/`, `docs/api/` |
| Design | `docs/design/` |
| Frontend | `frontend/` |
| Backend | `backend/` |
| AI/ML | `ai/` |
| Database | `database/` |
| DevOps | `infra/`, `.github/`, Dockerfiles |
| QA | `tests/e2e/` |
| Security | `docs/security/` |
| Documentation | `docs/runbook/`, `README.md`, `CHANGELOG.md` |
| Code Review | no product source — PR comments and/or `docs/reviews/` |
| JARVIS | platform state (Postgres), not product source |

A worker must not write outside its scope.

---

## 9. Proof of life (the only demo that counts)

**Command (or equivalent API):**

```text
jarvis build "Build a todo API with one authenticated list endpoint"
```

**Pass criteria — all required:**

1. JARVIS creates a task graph in Postgres.
2. One worker runs with a scoped workspace.
3. At least one commit exists on a feature branch.
4. A PR (or merge request) exists against `develop`.
5. Task status is `completed` or `failed` with a structured result — never hung forever (timeout configured; drill is Phase 5).
6. Token usage is recorded for every LLM call via the router.
7. Killing JARVIS mid-run and restarting does not lose the task row (checkpoint exists). Full kill-recovery *testing* is Phase 5; the checkpointer must already be wired.
8. Proof may use a stub CLI (`jarvis build`). Full CLI is Phase 6.

---

## 10. Work order (do not reorder)

1. Monorepo scaffold + git (`develop` branch exists)
2. Postgres + LangGraph checkpointer
3. Task DAG + assignment (even if the "agent" is a dummy node)
4. Model router + multi-provider transport + agent map + tier field on tasks
5. Worker integration (OpenHands, then fallback if blocked)
6. Wire dummy/real agent → branch → PR
7. Proof of life run, then fix seams

---

## 11. Exit gate (Phase 2 may not start until)

- [ ] Postgres checkpointer proven (restart retains state)
- [ ] Worker can create a branch and commit inside scope
- [ ] Model-router calls are logged with cost and provider `source`
- [ ] Task JSON in / JSON out contracts implemented (`intent_id`, `correlation_id`)
- [ ] Platform root and product tree both exist (C1)
- [ ] Artifact directories exist
- [ ] Task timeout configured (default 30 min)
- [ ] Proof of life documented (command, repo, PR link, what failed)
- [ ] OpenHands vs fallback decision written in `docs/runbook/` (one page)

---

## 12. Failure modes (check these first)

| Symptom | Likely cause |
|---|---|
| Graph runs once then amnesia | Checkpointer not actually attached |
| Worker "succeeds" with no git changes | Lifecycle / working directory wrong |
| Windows + Docker mount empty | WSL2 path / volume bind |
| Token log missing | Calls bypassing the model router |
| Hung task | No timeout; add hard task timeout in this phase (default 30 min) |

---

## 13. Time truth

LangGraph learning + OpenHands/Docker on Windows will dominate. Budget **days**, not the sum of "3 hours + 6 hours." Constitution over schedule: a working loop on day 4 beats a perfect OpenHands integration with no PR.
