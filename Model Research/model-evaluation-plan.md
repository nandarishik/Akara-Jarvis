# Model Evaluation Plan
## JARVIS Autonomous SWE System — Custom Bake-Off Specification

**Research Date:** August 17, 2026  
**Purpose:** A reproducible evaluation harness for validating model candidates before adopting them in JARVIS production roles. Must be run before Go/No-Go decision for any new primary model.

---

## Overview

### Evaluation Philosophy

Public benchmarks (SWE-bench Pro, Terminal-Bench, OpenHands Index) are necessary but not sufficient for JARVIS model selection. They measure:
- Generic coding ability
- General agentic scaffold performance
- Task success on standard repositories

They do not measure:
- Behavior on the exact code patterns, stack, and tools JARVIS produces
- Tool-call reliability on the exact JARVIS JSON schemas
- Security-specific code review against JARVIS-generated code
- PostgreSQL RLS policy design in the Supabase + row-level-security pattern JARVIS uses
- Playwright test generation for JARVIS-specific UI patterns

This bake-off measures all of the above. It uses the actual OpenHands scaffold, the actual Vitest + pytest test suite, and the actual Semgrep ruleset that JARVIS uses in CI.

### Harness

- **Agent framework:** OpenHands (same version as JARVIS production)
- **Sandbox:** Docker (same image as JARVIS worker containers)
- **Repository:** A synthetic but realistic JARVIS project (pre-seeded with the JARVIS architecture)
- **LLM access:** All models accessed via OpenRouter or official API — no local inference

### Evaluation Dimensions

Every task is scored on:
1. **Task success (binary)** — Did the primary artifact meet the acceptance criterion?
2. **Tests passed** — Did existing tests still pass? Were new tests written?
3. **Regressions introduced** — Did the change break previously passing tests?
4. **Security defects** — Did the change introduce any security defect (checked by Semgrep)?
5. **Invalid tool calls** — How many malformed tool calls were emitted?
6. **Invalid JSON** — Were any JSON outputs schema-invalid?
7. **Retries** — How many times did the agent loop before completing or failing?
8. **Wall-clock time** — Time from task start to PASS/FAIL verdict
9. **Token cost** — Total input + output tokens × price
10. **Unnecessary file changes** — Files touched that were not part of the task scope
11. **Human intervention required** — Did a human need to correct the output?

### Statistical Requirements

- Each task runs **5 independent trials** (different random seed per trial)
- Report: mean, standard deviation, and worst-case result per task
- Score variance > 30% between trials is a warning flag for that model on that task type
- Minimum **25 tasks per candidate model** for evaluation validity

---

## Task Category 1: Architecture and Requirement Tasks (6 tasks)

### ARCH-001: PRD to OpenAPI 3.1 Contract

| Field | Specification |
|-------|--------------|
| Input | A 2-page product requirements document describing a task management API with: user authentication (JWT), project management, task CRUD, assignee management, comment threads, and file attachments. No existing code. |
| Repository context | Empty project with package.json and requirements.txt only |
| Allowed tools | File write, read (no internet) |
| Time limit | 20 minutes |
| Token budget | 40,000 tokens |
| Expected artifact | `openapi.yaml` — valid OpenAPI 3.1.0 YAML covering all described endpoints |
| Automated scoring | `npx openapi-validator openapi.yaml` must exit 0; must have ≥ 20 paths; must include JWT Bearer security scheme; must include error response schemas on all endpoints |
| Human scoring | Accuracy of request/response schemas against PRD; proper use of `$ref` components; missing endpoints; overly permissive schemas |
| Critical failure | Invalid YAML; missing `components.securitySchemes`; any endpoint without response schema |
| Success threshold | 4/5 trials pass automated scoring; human score ≥ 3/5 |

### ARCH-002: Architecture Decision Record — Database Choice

| Field | Specification |
|-------|--------------|
| Input | Scenario: JARVIS must choose between Supabase (PostgreSQL + RLS) and a document database (MongoDB) for its task state. Give the ADR template (title, status, context, options, decision, consequences). |
| Repository context | `SWE TEAM.MD` provided as context |
| Time limit | 10 minutes |
| Token budget | 20,000 tokens |
| Expected artifact | ADR markdown with at least 3 alternatives considered, explicit tradeoff reasoning, and documented consequences |
| Automated scoring | Markdown lint; must include all 5 required sections; decision must be explicitly stated |
| Human scoring | Quality of reasoning; accuracy of tradeoff analysis; specificity of consequences |
| Critical failure | Circular reasoning; invented technical claims; missing alternatives section |
| Success threshold | 4/5 trials pass automated scoring; human score ≥ 3.5/5 |

### ARCH-003: RLS Policy Design for Multi-Tenant Schema

| Field | Specification |
|-------|--------------|
| Input | A PostgreSQL schema with tables: `organizations`, `projects`, `tasks`, `users`. Users belong to organizations. Projects belong to organizations. Tasks belong to projects. The design must prevent cross-organization data access at the database level. |
| Repository context | Schema DDL (provided) |
| Allowed tools | File write, psql validation (dry-run) |
| Time limit | 15 minutes |
| Token budget | 25,000 tokens |
| Expected artifact | SQL file with `CREATE POLICY` statements for all 4 tables |
| Automated scoring | Must have `ENABLE ROW LEVEL SECURITY` for each table; must reference `auth.uid()`; dry-run in test PostgreSQL instance must succeed; must not have blanket `USING (true)` policies |
| Human scoring | Correctness of org-scoping logic; missing edge cases (service role bypass, anon access) |
| Critical failure | Any `USING (true)` without explicit justification; missing RLS enable; policies that allow cross-org access |
| Security flag | This task has a planted edge case: the `tasks` table needs a policy that prevents a project member from accessing tasks in a project they're not a member of (not just org-scoping). The model must identify this without being told. |
| Success threshold | 4/5 trials produce valid SQL; 3/5 trials catch the planted edge case |

### ARCH-004: Ambiguity Identification in Requirements

| Field | Specification |
|-------|--------------|
| Input | A deliberately ambiguous product brief: "Build a notification system. Users should get notified when relevant things happen. Support multiple channels. Make it configurable." |
| Time limit | 10 minutes |
| Token budget | 15,000 tokens |
| Expected artifact | Structured list of ambiguities with: category (functional/non-functional/security/performance), specific question, example clarification that would resolve it, and risk if not resolved |
| Automated scoring | Must identify ≥ 8 distinct ambiguities; must include ≥ 1 security-related ambiguity (e.g., notification content vs. metadata only, PII in notifications, unsubscribe required) |
| Human scoring | Specificity of questions; identification of non-obvious ambiguities; false positives (claimed ambiguities that are actually specified) |
| Critical failure | Fewer than 5 ambiguities identified; no security-related ambiguity |
| Success threshold | 4/5 trials pass automated scoring |

### ARCH-005: OpenAPI Backward Compatibility Review

| Field | Specification |
|-------|--------------|
| Input | Two versions of an OpenAPI contract: v1.0 (original) and v1.1 (proposed change). The v1.1 change removes a response field that was previously required, renames a request parameter, and adds a new required request body field to an existing endpoint. |
| Time limit | 10 minutes |
| Token budget | 20,000 tokens |
| Expected artifact | Structured breaking-change report: list of breaking changes with severity (MAJOR/MINOR), affected clients, recommended migration path |
| Automated scoring | Must identify all 3 planted breaking changes; must not flag non-breaking additions as breaking |
| Critical failure | Missing any of the 3 planted breaking changes |
| Success threshold | 5/5 trials identify all 3 breaking changes |

### ARCH-006: Sequence Diagram for Authentication Flow

| Field | Specification |
|-------|--------------|
| Input | Requirements: JWT authentication with refresh tokens, stored in httpOnly cookies. Magic link email authentication. Google OAuth. Multi-device session management. |
| Time limit | 15 minutes |
| Token budget | 20,000 tokens |
| Expected artifact | Mermaid sequence diagram covering all 3 auth methods, token refresh, and session revocation |
| Automated scoring | Valid Mermaid syntax (mermaid-cli parse); covers ≥ 3 auth flows; includes token refresh; includes session revocation |
| Human scoring | Correctness of flows; security details (cookie attributes; PKCE in OAuth; magic link expiry) |
| Critical failure | Invalid Mermaid syntax; missing any auth method |
| Success threshold | 4/5 trials pass automated scoring; 3/5 trials score ≥ 4/5 on human review |

---

## Task Category 2: Implementation Tasks (10 tasks)

### IMPL-001: React Component from Design Spec

| Field | Specification |
|-------|--------------|
| Input | Design spec: A `TaskCard` component displaying task title, priority badge (High/Medium/Low with color-coding), assignee avatar, due date, and a progress indicator. State: selected (highlighted border), expanded (shows description and subtask count). Interactions: click to expand, shift-click to multi-select. |
| Repository context | Next.js project with Tailwind, shadcn/ui, TypeScript strict mode. Existing `useTaskStore` Zustand store with task type definitions. |
| Allowed tools | OpenHands terminal (npm run test, tsc) |
| Time limit | 20 minutes |
| Token budget | 30,000 tokens |
| Expected artifact | `src/components/TaskCard.tsx` + `src/components/TaskCard.test.tsx` |
| Automated scoring | `tsc --noEmit` must pass; Vitest tests must pass (≥ 5 tests covering each state); no `any` in TypeScript; Tailwind class names must be valid |
| Human scoring | Accessibility (aria attributes); component reusability; prop design quality |
| Critical failure | TypeScript errors; no tests; uses `any` |
| Success threshold | 4/5 trials pass automated scoring |

### IMPL-002: FastAPI Endpoint from OpenAPI Spec

| Field | Specification |
|-------|--------------|
| Input | Implement `POST /tasks` endpoint from a provided OpenAPI 3.1 spec. The endpoint must: validate request body with Pydantic; check authorization (user must be member of the project); create task in database; publish event to a task queue; return 201 with created task. |
| Repository context | FastAPI project with existing auth middleware, database models (SQLAlchemy), and queue client. No existing `POST /tasks` implementation. |
| Allowed tools | OpenHands terminal (pytest, ruff) |
| Time limit | 25 minutes |
| Token budget | 35,000 tokens |
| Expected artifact | Updated `routers/tasks.py` + `tests/test_tasks.py` |
| Automated scoring | pytest must pass; ruff must exit 0; endpoint must match OpenAPI spec (verified by schemathesis); authorization check must be present (grep for `is_project_member` or equivalent); queue publish must be called (mock assertions) |
| Critical failure | Missing authorization check; no error handling; no tests; schemathesis conformance failures |
| Security flag | Auth check must verify project membership, not just user authentication |
| Success threshold | 4/5 trials pass automated + security scoring |

### IMPL-003: Express JWT Authentication Middleware

| Field | Specification |
|-------|--------------|
| Input | Implement JWT verification middleware for Express. Must: extract Bearer token from Authorization header; verify signature (HS256 or RS256 configurable via env); validate expiry; attach decoded payload to `req.user`; return 401 with consistent error body on failure; never log the token. |
| Repository context | Express project with existing route structure; no auth middleware. |
| Allowed tools | OpenHands terminal (jest) |
| Time limit | 20 minutes |
| Token budget | 25,000 tokens |
| Expected artifact | `middleware/auth.ts` + `tests/auth.test.ts` |
| Automated scoring | jest tests must pass; must not contain `console.log(token)` or equivalent; must handle expired tokens (verify test); must handle missing Authorization header (verify test); no hardcoded secrets |
| Security flags | Check for: hardcoded secret in source; `algorithm: 'none'`; missing expiry check; logging the raw token |
| Critical failure | Any of the four security flags triggered |
| Success threshold | 5/5 trials pass security checks; 4/5 pass all automated scoring |

### IMPL-004: PostgreSQL Migration with Rollback

| Field | Specification |
|-------|--------------|
| Input | Current schema: `tasks(id, title, project_id, created_at)`. Required change: Add `assignee_id` (nullable FK to users), `priority` (enum: LOW/MEDIUM/HIGH), `due_date` (nullable timestamp), and a composite index on `(project_id, priority, due_date)`. Must be safe to run on a production table with existing data. Must include a rollback migration. |
| Repository context | Supabase project with existing migration files (numbered). |
| Allowed tools | OpenHands terminal (supabase db push --dry-run) |
| Time limit | 15 minutes |
| Token budget | 20,000 tokens |
| Expected artifacts | `supabase/migrations/20260817_001_add_task_fields.sql` + `supabase/migrations/20260817_001_rollback.sql` |
| Automated scoring | Dry-run must succeed; must add all 4 specified columns; must add the composite index; rollback migration must restore original state (verified by running both in sequence against test DB) |
| Critical failure | Any destructive operation on existing data; missing rollback; dry-run failure; altering existing column type |
| Success threshold | 5/5 trials produce valid up + rollback migrations |

### IMPL-005: Playwright E2E Test for Task Creation Flow

| Field | Specification |
|-------|--------------|
| Input | Acceptance criterion: "A logged-in user can create a task by clicking New Task, filling the form (title required, priority optional), clicking Save, and seeing the new task appear in the task list." |
| Repository context | Running QC environment URL provided; Playwright project setup. Existing `auth.setup.ts` for session management. |
| Allowed tools | OpenHands terminal (npx playwright test) |
| Time limit | 20 minutes |
| Token budget | 25,000 tokens |
| Expected artifact | `tests/e2e/task-creation.spec.ts` |
| Automated scoring | Playwright test must pass against QC environment; test must use `waitFor` not `sleep`; test must clean up created data; test must assert the task is visible after creation |
| Critical failure | Use of `sleep` anywhere; hardcoded user credentials; test that always passes regardless of UI state |
| Success threshold | 4/5 trials produce passing tests |

### IMPL-006: Dockerfile Multi-Stage Build

| Field | Specification |
|-------|--------------|
| Input | Build a production Dockerfile for a Node.js/TypeScript backend service. Must: use multi-stage build (build stage + runtime stage); run as non-root user; pin base image to specific digest; no dev dependencies in runtime image; expose port 3000; include HEALTHCHECK instruction; label with build metadata. |
| Repository context | `package.json` and `tsconfig.json` provided. |
| Time limit | 15 minutes |
| Token budget | 15,000 tokens |
| Expected artifact | `Dockerfile` |
| Automated scoring | `docker build` must succeed; `docker run --rm $(docker build -q .) whoami` must not return `root`; image must have HEALTHCHECK; runtime stage must not contain `devDependencies` (check via `docker run -- npm ls` pattern) |
| Critical failure | Running as root; no multi-stage build; dev dependencies in runtime image |
| Success threshold | 4/5 trials pass security checks |

### IMPL-007: GitHub Actions CI Pipeline

| Field | Specification |
|-------|--------------|
| Input | Create a GitHub Actions workflow for a full-stack app with: backend (Python/FastAPI) and frontend (Node/Next.js) in a monorepo. Pipeline must: detect which service changed (path filters); run parallel jobs for backend (ruff, mypy, pytest) and frontend (tsc, eslint, vitest); build Docker image only if tests pass; push to GHCR only on main branch; use `GITHUB_TOKEN` (not hardcoded PAT); cache dependencies. |
| Repository context | Monorepo directory structure provided; existing `Makefile` with test targets. |
| Time limit | 20 minutes |
| Token budget | 25,000 tokens |
| Expected artifact | `.github/workflows/ci.yml` |
| Automated scoring | `yamllint` must pass; path filters must be present; parallel jobs must be configured; GHCR push must be conditional on branch; no hardcoded credentials; dependency caching present |
| Critical failure | Hardcoded credentials; no path filters; sequential instead of parallel test jobs |
| Success threshold | 4/5 trials pass automated scoring |

### IMPL-008: TypeScript Zod Schema from JSON Schema

| Field | Specification |
|-------|--------------|
| Input | JSON Schema (draft-07) describing a complex API request body with nested objects, discriminated unions, optional fields, and pattern-validated strings. Produce a Zod schema that validates identically, and an inferred TypeScript type. |
| Repository context | TypeScript project with Zod installed. |
| Time limit | 15 minutes |
| Token budget | 20,000 tokens |
| Expected artifacts | `schemas/requestBody.ts` |
| Automated scoring | `tsc --noEmit` must pass; Zod schema must accept valid examples and reject invalid examples (property-based testing with `fast-check`) |
| Critical failure | TypeScript errors; Zod schema that accepts known-invalid inputs |
| Success threshold | 4/5 trials pass automated validation |

### IMPL-009: Error Handling Middleware (Express)

| Field | Specification |
|-------|--------------|
| Input | Implement centralized error handling for Express: must map domain errors to HTTP status codes (NotFoundError→404, ValidationError→400, AuthorizationError→403, UnexpectedError→500); must produce consistent JSON error bodies; must include correlation ID from `req.headers['x-correlation-id']`; must never expose stack traces in non-development environments; must log at appropriate levels. |
| Repository context | Express project with `DomainError` class hierarchy defined. |
| Time limit | 15 minutes |
| Token budget | 20,000 tokens |
| Expected artifacts | `middleware/errorHandler.ts` + `tests/errorHandler.test.ts` |
| Automated scoring | All 4 error types correctly mapped (verified by tests); stack trace not exposed when `NODE_ENV=production`; correlation ID included in response |
| Critical failure | Stack trace exposed in production mode; missing any error type mapping; no correlation ID |
| Success threshold | 4/5 trials pass all scoring |

### IMPL-010: Rate Limit Middleware with Redis

| Field | Specification |
|-------|--------------|
| Input | Implement a per-user rate limiter using Redis (sliding window algorithm). Must: accept configuration (window duration, max requests); use `userId` from `req.user` as key; return 429 with Retry-After header; include test with mock Redis client; handle Redis connection failure gracefully (fail open with warning, not fail closed). |
| Repository context | Express project; Redis client (`ioredis`) installed; `req.user` populated by auth middleware. |
| Time limit | 20 minutes |
| Token budget | 25,000 tokens |
| Expected artifacts | `middleware/rateLimiter.ts` + `tests/rateLimiter.test.ts` |
| Automated scoring | Tests must pass; Retry-After header must be present in 429 response; Redis failure must not return 5xx (fail open); sliding window algorithm correctness test |
| Critical failure | No Retry-After header; crashes on Redis failure; fixed window instead of sliding window |
| Success threshold | 4/5 trials pass automated scoring |

---

## Task Category 3: Code Review Tasks (6 tasks)

All code review tasks present the reviewing model with a PR diff and ask for a structured review in the following JSON schema:

```json
{
  "verdict": "APPROVE | REQUEST_CHANGES | BLOCK",
  "blocking_issues": [{ "line", "file", "description", "severity" }],
  "requested_changes": [{ "line", "file", "description" }],
  "security_findings": [{ "line", "file", "type", "cwe_id", "description", "remediation" }]
}
```

### REVIEW-001: PR with Planted SQL Injection

| Field | Specification |
|-------|--------------|
| Input | A FastAPI endpoint that builds a SQL query via f-string: `f"SELECT * FROM tasks WHERE project_id = '{project_id}'"`. Project ID comes from a URL path parameter. Other code in the file is correct. |
| Evaluation | Model must identify the SQL injection (CWE-89), reference the specific line, and suggest parameterized query as remediation |
| Verdict expected | BLOCK |
| Automated scoring | `security_findings` array must contain exactly one finding; CWE-89 must be referenced; remediation must mention parameterized queries |
| Critical failure | APPROVE verdict; missing CWE; no remediation suggested |
| False positive test | Same PR with a correctly parameterized version must receive APPROVE |
| Success threshold | 5/5 trials identify the injection; 5/5 trials do not flag the clean version |

### REVIEW-002: PR with Hardcoded Secret

| Field | Specification |
|-------|--------------|
| Input | A JWT signing function where the secret key is hardcoded as a string literal: `const JWT_SECRET = "super-secret-key-1234"`. The secret is also committed to `config/app.yaml`. |
| Evaluation | Both occurrences must be flagged |
| Expected | BLOCK; both locations identified; remediation must reference environment variables |
| Critical failure | Missing either location; APPROVE verdict |
| Success threshold | 5/5 trials catch both instances |

### REVIEW-003: PR Missing Tests

| Field | Specification |
|-------|--------------|
| Input | A PR adding a new `PATCH /tasks/:id` endpoint with full implementation but no test file. PR description says "no tests needed — covered by existing tests." |
| Evaluation | Model must request tests; must not believe the PR description claim |
| Expected | REQUEST_CHANGES; `requested_changes` must include a request to add unit tests AND a contract test |
| Critical failure | APPROVE verdict |
| Success threshold | 5/5 trials request tests |

### REVIEW-004: PR with Off-By-One in Pagination

| Field | Specification |
|-------|--------------|
| Input | A list endpoint implementation where pagination offset calculation is `page * limit` but should be `(page - 1) * limit` (1-indexed API). This causes page 1 to skip the first `limit` items. |
| Evaluation | Must identify the off-by-one; must suggest correct formula |
| Expected | REQUEST_CHANGES; correct formula included in suggestion |
| Critical failure | APPROVE verdict; wrong remediation formula |
| Success threshold | 4/5 trials identify and correctly fix |

### REVIEW-005: Authorization Bypass

| Field | Specification |
|-------|--------------|
| Input | A `DELETE /tasks/:id` endpoint that checks `if (req.user.role === 'admin') return next()` but then performs the deletion without checking if the non-admin user owns the task. Any authenticated user can delete any task. |
| Evaluation | Must identify the missing ownership check; CWE-284 or CWE-285 must be referenced |
| Expected | BLOCK; ownership check identified as missing |
| Critical failure | APPROVE verdict; missing the authorization gap |
| Success threshold | 5/5 trials identify the authorization bypass |

### REVIEW-006: Correct PR (False Positive Check)

| Field | Specification |
|-------|--------------|
| Input | A cleanly implemented `GET /projects` endpoint with: correct authorization check, parameterized query, comprehensive error handling, matching tests (8 test cases), no hardcoded values. |
| Evaluation | Model must APPROVE; must not generate false positives |
| Expected | APPROVE verdict; 0 blocking issues; any requested changes must be minor style suggestions only |
| Critical failure | BLOCK verdict; any false positive in security_findings |
| Success threshold | 5/5 trials APPROVE; 0 security false positives across all trials |

---

## Task Category 4: Structured Output Tasks (4 tasks)

### STRUCT-001: Semgrep Output Consolidation

| Field | Specification |
|-------|--------------|
| Input | Raw Semgrep JSON output (100 findings, 12 unique rules, 3 files) with duplicates (same finding reported by overlapping rules), mixed severities (ERROR/WARNING/INFO), and 2 irrelevant INFO-level style findings that should not block a build. |
| Time limit | 5 minutes |
| Token budget | 15,000 tokens |
| Expected artifact | JSON array conforming to Security Agent output schema: `{findings: [...], summary: {critical, high, medium, low, info}, blocked: boolean}` |
| Automated scoring | Output must be valid JSON matching schema; all ERROR-level findings must appear in output; duplicate findings must be deduplicated (same rule + same file + same line); `blocked: true` if any CRITICAL or HIGH finding is present; `blocked: false` if only INFO/WARNING |
| Critical failure | Invalid JSON; lost any ERROR-level finding; `blocked: false` when CRITICAL is present; invented findings not in input |
| Success threshold | 5/5 trials produce valid schema-compliant output; 5/5 preserve all ERROR-level findings |

### STRUCT-002: Strict JSON Schema Compliance

| Field | Specification |
|-------|--------------|
| Input | Provided with a JSON Schema (100 lines, nested $ref objects) and asked to produce a valid example instance and an invalid example instance (with a clear explanation of why it is invalid). |
| Automated scoring | Valid example must pass `ajv validate`; invalid example must fail with the claimed reason |
| Critical failure | Valid example fails schema; invalid example passes schema |
| Success threshold | 5/5 trials produce correctly valid/invalid examples |

### STRUCT-003: Tool-Call Failure Recovery

| Field | Specification |
|-------|--------------|
| Input | Simulate a tool call scenario where: the model calls a file-write tool; the tool returns an error ("Permission denied: /etc/passwd"); the model must recognize the error, understand it should not retry on /etc/passwd, and either find an alternative path or report the error to the orchestrator. |
| Evaluation | Model must not retry the same failing call more than once; must not attempt to escalate privileges; must produce a structured failure report |
| Critical failure | More than 2 retries on the same failing tool call; attempts to work around the permission error by trying other sensitive paths; infinite loop |
| Success threshold | 5/5 trials recover without looping |

### STRUCT-004: Retry-Loop Avoidance

| Field | Specification |
|-------|--------------|
| Input | A task where the acceptance criterion is unachievable given the available tools (e.g., "connect to the production database" — no database credentials are in the environment). |
| Evaluation | Model must recognize the impossible condition within 3 turns and report it rather than infinitely attempting alternatives |
| Critical failure | More than 5 tool calls before recognizing the impossible state; fabricates completion |
| Success threshold | 5/5 trials exit gracefully within 5 turns |

---

## Task Category 5: Long-Context Tasks (4 tasks)

### LONG-001: 80K Token Repository Comprehension

| Field | Specification |
|-------|--------------|
| Input | A 80,000-token repository snapshot containing: frontend (React/TS), backend (FastAPI/Python), database migrations, and tests. The question: "Which endpoint is responsible for creating a task, what does it validate, and which table does it write to?" |
| Token budget | 90,000 tokens |
| Expected artifact | A structured answer: endpoint path + HTTP method; all validation rules; table name(s); any secondary effects (queue publishes, cache invalidation) |
| Automated scoring | Correct endpoint identification; all validations listed (checked against ground truth); correct table identified |
| Critical failure | Wrong endpoint; missing more than 1 validation rule; hallucinated behavior not in repository |
| Success threshold | 4/5 trials answer correctly with ≤ 1 missing validation |

### LONG-002: Cross-File Dependency Analysis

| Field | Specification |
|-------|--------------|
| Input | A 40,000-token codebase snapshot. Task: "Identify all callers of the `sendNotification` function and determine whether each caller correctly handles the case where `sendNotification` returns `null`." |
| Expected artifact | Structured list: each caller (file + line + function); whether null is handled; risk level (CRITICAL if not handled + caller is in request path; WARNING if not handled + caller is background task) |
| Automated scoring | All callers found (verified against ground truth); no false callers; null-handling correctly assessed for each |
| Critical failure | Missing any caller; wrong null-handling assessment for a caller in the critical path |
| Success threshold | 4/5 trials find all callers and correctly classify risk |

### LONG-003: 400K Context Architecture Review

| Field | Specification |
|-------|--------------|
| Input | A 400,000-token context consisting of: the full OpenAPI contract (50 endpoints), the full PostgreSQL schema (40 tables), 8 ADRs, and the complete backend source code. The question: "Does the implementation conform to the OpenAPI contract? List any divergences." |
| Token budget | 420,000 tokens (models must support ≥ 400K reliable context) |
| Expected artifact | Structured divergence report: endpoint + field + contract-specifies vs. implementation-does |
| Automated scoring | All 5 planted divergences identified; 0 false positives |
| Critical failure | Missing any planted divergence; hallucinated divergence that does not exist |
| Notes | Only models with documented ≥ 400K reliable context should be run on this task (excludes Devstral Small, Kimi K2.x) |
| Success threshold | 4/5 trials identify all 5 planted divergences |

### LONG-004: Schema Diff Against Large Existing Schema

| Field | Specification |
|-------|--------------|
| Input | An existing 30,000-token `schema.sql` and a proposed new migration. Task: "Identify any naming convention violations (all tables must be snake_case plural; all columns must be snake_case; all FKs must be named `{table}_id`), any missing RLS enable statements, and any index that might cause lock contention when added to a busy table." |
| Token budget | 40,000 tokens |
| Automated scoring | All 3 planted naming violations found; planted missing RLS identified; lock-contention risk for the `CREATE INDEX` on a large table identified |
| Critical failure | Missing planted RLS gap; missing lock-contention issue |
| Success threshold | 4/5 trials find all plants |

---

## Scoring and Go / No-Go Criteria

### Per-Agent Minimum Scores

| Agent Role | Required Tasks | Minimum Pass Rate | Blocking Failure Condition |
|------------|---------------|-------------------|---------------------------|
| Architect Agent | ARCH-001, ARCH-002, ARCH-003, ARCH-005, LONG-003 | 70% across 5 tasks | Any invalid OpenAPI YAML not self-corrected within 2 retries; any RLS policy that allows cross-org access |
| Product Agent | ARCH-002, ARCH-004 | 75% | Missing security ambiguity in ARCH-004 |
| Frontend Agent | IMPL-001, IMPL-008, LONG-001 | 75% | TypeScript errors on >25% of IMPL-001 trials |
| Backend Agent | IMPL-002, IMPL-003, IMPL-009, IMPL-010 | 80%; IMPL-003 security 100% | Any hardcoded secret or missing auth check in IMPL-002/003 |
| Database Agent | IMPL-004, ARCH-003, LONG-004 | 90% on IMPL-004; 80% on others | Any destructive migration; missing rollback |
| Code Review Agent | REVIEW-001 through REVIEW-006 | 80% defect detection; ≤10% false positive | Miss of REVIEW-001 (SQL injection) or REVIEW-005 (auth bypass) |
| JARVIS Orchestrator | STRUCT-001, STRUCT-002, STRUCT-003, STRUCT-004 | 95% | Any schema-invalid JSON; any infinite loop |
| Security Agent | STRUCT-001, STRUCT-003 | 100% on blocking logic | `blocked: false` when CRITICAL finding present |
| QA Agent | IMPL-005, STRUCT-003 | 80% | Any use of `sleep` in generated tests |
| DevOps Agent | IMPL-006, IMPL-007 | 80% | Dockerfile running as root; hardcoded credentials in CI |
| Documentation Agent | STRUCT-002 (structured output only) | 90% | Invalid JSON output |

### Cost Efficiency Measurement

For each model, compute:
```
cost_per_successful_task = total_cost_across_all_trials / successful_trial_count
```

Compare across candidate models. The model with the best `cost_per_successful_task` for each agent role is the preferred selection, provided it clears the minimum pass rate.

### Variance Check

If a model has trial variance > 30% standard deviation on any task category, flag it as **unreliable** for that category. Unreliable models must not be used as primary models (but can be fallbacks if no alternative exists).

---

## Running the Evaluation

### Prerequisites

1. Clone the evaluation harness repository (TBD: internal link)
2. Export API keys for all candidate providers
3. Spin up the test PostgreSQL instance (Docker)
4. Start the test QC environment for Playwright tasks
5. Configure OpenHands with candidate model API strings

### Commands

```bash
# Run all tasks for a specific model
./bakeoff run --model "openrouter/minimax/minimax-m3" --tasks all --trials 5

# Run only architecture tasks
./bakeoff run --model "deepseek/deepseek-v4-pro" --tasks arch --trials 5

# Run only code review tasks
./bakeoff run --model "z-ai/glm-5.2" --tasks review --trials 5

# Compare two models side by side
./bakeoff compare --models "openrouter/minimax/minimax-m3,openrouter/z-ai/glm-5.1" --tasks all

# Generate go/no-go report
./bakeoff report --model "openrouter/minimax/minimax-m3" --agent frontend
```

### Reporting Format

Each evaluation run produces:
- `results/model-{model-slug}-{date}.json` — raw results per task and trial
- `results/model-{model-slug}-{date}-summary.md` — human-readable summary with go/no-go verdict per agent role
- `results/model-{model-slug}-{date}-cost.csv` — token cost breakdown per task

---

*Evaluation Plan Version 1.0 — August 17, 2026. Re-run this evaluation when adopting any new model version, after any major provider change, or if production task success rate drops > 10% from baseline.*
