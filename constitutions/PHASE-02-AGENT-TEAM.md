# Phase 2 Constitution — Agent Team

**Duration:** 2–3 days (expect prompt iteration to fill it)  
**Depends on:** Phase 1 Exit Gate  
**Unlocks:** Phase 3  
**Parent:** [`../SWE TEAM.MD`](../SWE%20TEAM.MD) · Index: [`PHASES.md`](PHASES.md)

This phase makes JARVIS a team, not a single worker. The bottleneck is prompt quality and artifact handoffs, not YAML.

---

## 1. Purpose

Install every agent as a LangGraph node with a **role prompt**, **scope**, **default model tier**, and **artifact contract**. Prove that Agent A's files are valid input for Agent B. Install Code Review as a **real gate**. Install budgets, circuit breakers, and the dead letter queue.

---

## 2. Non-negotiables

1. **Plans before code.** No Frontend/Backend/AI/DB engineering task starts until:
   - Product Agent has committed acceptance criteria (Given/When/Then)
   - Architect Agent has committed OpenAPI 3.1 contracts
2. Design Agent may run **in parallel** with Architect after Product completes. Frontend may not start until Design tokens + component spec exist **and** Architect contracts exist.
3. **Author cannot approve.** Code Review Agent is a separate node. Self-approval is a constitutional crime.
4. Code Review does **not** nanny style. ESLint, Prettier, Ruff own formatting. Review owns spec match, bugs, tests, security anti-patterns, error handling.
5. Max **3** retries per **issue_key** (index **C4**). Fourth failure on that issue → dead letter + human. No silent retry storms.
6. Agents do not DM each other. They write files. JARVIS reads structured results.
7. Vague Product criteria ("should be fast") are **rejected**. Specific criteria only.
8. Tiers follow index **C3** (Architect = 3, not "Tier 1 Opus" prose in `SWE TEAM.MD` §3).
9. Database Agent does not write migrations until Architect has committed schema (in ADRs/`docs/api/` or `database/schema.sql` draft). Frontend does not start without Design **and** OpenAPI. Backend may start from OpenAPI without Design.
10. Accessibility floor: **WCAG 2.1 AA** in Design specs; Frontend must implement the callouts.

---

## 3. The thirteen roles (all must exist as nodes)

A node that only logs "not implemented" is illegal in Phase 2 **except** as a temporary stub lasting **less than one working day**. By Exit Gate, every role below has a prompt and can produce its artifact type (even if quality will improve later).

| Agent | Primary (Portfolio B) | Fallback / escalate | OpenHands | Tier class |
|---|---|---|---|---|
| JARVIS | DeepSeek V4 Flash | GPT-OSS-120B (Groq) | No | 1–2 |
| Product | DeepSeek V4 Pro | Kimi K2.6 → GLM-5.2 | No | 2→3 |
| Architect | DeepSeek V4 Pro | GLM-5.2 → Kimi K3 | No | **always 2–3** |
| Design | MiniMax M3 (vision) | Kimi K2.5 | No | 0–1 |
| Frontend | MiniMax M3 | Kimi → V4 Pro | Yes | 0→2 |
| Backend | MiniMax M3 | Kimi → V4 Pro; auth → V4 Pro + Kimi K3 review | Yes | 0→3 |
| AI/ML | Kimi K2.6 | MiniMax → V4 Pro | Yes | 2 |
| Database | MiniMax M3 | Kimi → V4 Pro; prod migration / RLS escalate | Yes | 0→3 |
| Code Review | GLM-5.2 | V4 Pro; high-risk → Kimi K3 | No | 2→3 |
| QA | MiniMax M3 (vision) | Devstral → V4 Pro | Yes | 0→2 |
| Security | DeepSeek V4 Flash | GPT-OSS-120B | No | 0–1 |
| DevOps | MiniMax M3 | Devstral → V4 Pro | Yes | 0→2 |
| Documentation | DeepSeek V4 Flash | Devstral | No | 0 |

Authoritative IDs live in `config/model-routing.yaml`. Plus the **execution engine** is still OpenHands (or Phase 1 fallback), not a 15th "personality."

**Cross-family review:** Code Review’s model family **must differ** from the implementing agent’s family. High-risk paths (auth, payments, RLS, secrets, prod migrations, CI credentials) require escalation reviewer (Kimi K3) and may require human approval.

**Risk classifier:** JARVIS evaluates path/keyword patterns from `config/model-routing.yaml` `risk_classifier` before dispatch.

---

## 4. Design Agent law (applies to every product JARVIS builds)

Approved libraries only (MIT): ReactBits, shadcn/ui, Radix, Framer Motion, cmdk, Sonner, Vaul, React Email.

**Banned in specs and in Frontend output:**

- Card-grid-as-the-whole-product
- Purple/blue gradient CTAs with no design reason
- Centered hero + "Get Started" + stock illustration as the default landing
- Dashboard = identical metric cards with icon + number
- Raw `div` + Tailwind recreations of libraries the spec named

If the spec says ReactBits animated card, Frontend uses ReactBits. Animations in the spec are **not optional**.

---

## 5. Code Review law

**Position:** gates every PR to `develop`.

**Must check:**

- Implements the task spec (Product/Architect/Design artifacts)
- Matches existing patterns (RAG comes in Phase 6; until then, include `docs/api/contracts.yaml`, `database/schema.sql`, ADRs, tokens in the context package)
- Tests for new behavior
- Security anti-patterns (SQLi, XSS, secrets, permissive CORS)
- Error handling (no bare `catch`, no swallowed errors)

**Verdict schema (mandatory):**

```json
{
  "verdict": "approve | request_changes | block",
  "summary": "string",
  "comments": [
    { "path": "string", "line": 0, "what": "string", "why": "string" }
  ]
}
```

`request_changes` without *what* and *why* is invalid. JARVIS must not merge `request_changes` or `block`.

---

## 6. Context package (pre-RAG, still required)

Before every task, JARVIS assembles:

1. Role definition  
2. Project summary  
3. Task spec + acceptance criteria  
4. Relevant artifacts (contracts, design, schema)  
5. Previous attempts if retry (failure output + code that failed)

**Always include when present** (index **C5**):

- `docs/api/contracts.yaml`
- `database/schema.sql`
- `docs/architecture/decisions.md` (or ADRs folder)
- `docs/design/tokens.json`

Missing context the task depends on is a JARVIS bug, not an agent bug. Missing `tokens.json` during Product-only work is not a block.

---

## 7. Parallelism law

LangGraph parallel branches **must** be used as specified:

- After Product: Architect ∥ Design  
- After contracts + schema: Frontend ∥ Backend ∥ AI/ML. Database writes migrations only after Architect schema; do not let two agents rewrite the same migration files. Full migration lock is Phase 7.

Frontend and Backend share **OpenAPI as source of truth**. Neither invents endpoints.

---

## 8. Budgets, breakers, dead letters

**Token budget:** set per task from complexity. Over budget → JARVIS approves more tokens **or** reassigns model/agent. Agents cannot raise their own budget.

**Circuit breakers:**

- Task: 3 failures **per issue_key** → dead letter  
- Agent: 5 consecutive task failures → pause that agent, alert human  
- Budget: daily cap = monthly/30; non-critical pause (pause enforcement must be real in this phase)

**Dead letter table (required):**

```sql
CREATE TABLE dead_letter_tasks (
  task_id       UUID PRIMARY KEY,
  agent         TEXT NOT NULL,
  error_summary TEXT NOT NULL,
  full_context  JSONB NOT NULL,
  attempts      INT NOT NULL,
  created_at    TIMESTAMPTZ DEFAULT now(),
  resolved      BOOLEAN DEFAULT FALSE,
  resolution    TEXT
);
```

Human sees: what was tried, error output, generated code, original spec.

---

## 9. Handoff tests (this is the real work)

You are not done when prompts "sound good." You are done when this loop works on disk:

```
Product → Architect + Design
       → Database (migration files)
       → Backend (implements contract)
       → Frontend (consumes contract)
       → Code Review (approve or request_changes)
```

**Handoff failures to hunt:**

- Product stories with no Given/When/Then  
- OpenAPI that Frontend cannot generate types from  
- Design tokens JSON Frontend cannot parse  
- Backend routes that do not match the YAML  
- Reviewer commenting on Prettier issues  
- `needs_from` loops (A waits on B waits on A)

Run **at least two** distinct intents through planning + one coding agent + review (can be the same small app iterated).

---

## 10. Prompt iteration law

- 2–3 run/refine cycles per **critical** agent (Product, Architect, Design, Frontend, Backend, Code Review) are mandatory.
- Do not "finish" 13 first drafts and move on.
- Store prompts as **versioned files** under the **platform** repo (e.g. `jarvis/prompts/`), not inline strings.

**Coding-agent musts (from `SWE TEAM.MD`, enforced in prompts + review):**

- TypeScript strict; no `any`. API types from OpenAPI via `openapi-typescript` — no hand-rolled API DTOs.
- Frontend: container/presenter; keyboard + labels; new deps > 50KB need justification in the PR.
- Backend: schema validation every endpoint; structured errors; parameterized SQL; rate-limit middleware in the template (full numeric defaults Phase 7).
- AI/ML: prompts as versioned templates + eval pairs.

---

## 11. Out of scope

- Live GitHub Actions / cloud envs (Phase 3)
- Playwright against QC, ZAP execution (Phase 4) — schemas and prompts yes
- pgvector RAG (Phase 6)
- Production deploy (Phase 7)

---

## 12. Exit gate

- [ ] All **13** roles exist as nodes with versioned prompts (engine ≠ agent)
- [ ] Product + Architect gate engineering; Design gates Frontend
- [ ] Scopes match Phase 1 table (Code Review writes no product source)
- [ ] Architect ∥ Design after Product
- [ ] Code Review can `approve` / `request_changes` / `block` and JARVIS honors it
- [ ] Dead letter table + 3-retry + agent pause after 5 consecutive failures
- [ ] Token budget enforced (not just logged)
- [ ] Artifact handoff test recorded: paths, sample files, what broke, what was fixed
- [ ] No agent writes outside its filesystem scope
- [ ] Retries keyed by `issue_key` (C4)

---

## 13. Failure modes

| Symptom | Likely cause |
|---|---|
| Coding agents invent APIs | Contract missing from context package or Architect not actually gated |
| Review always approves | Prompt too weak; add forced spec-diff checklist |
| Review always blocks | Prompt too vague; require evidence per comment |
| Infinite `blocked` | `needs_from` not scheduled by JARVIS |
| Budget ignored | Worker bypassing the model router |
