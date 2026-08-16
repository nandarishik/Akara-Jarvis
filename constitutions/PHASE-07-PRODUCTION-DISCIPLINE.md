# Phase 7 Constitution — Production Discipline

**Duration:** 2–3 days  
**Depends on:** Phase 6 Exit Gate  
**Unlocks:** Phase 8  
**Parent:** [`../SWE TEAM.MD`](../SWE%20TEAM.MD) · Index: [`PHASES.md`](PHASES.md)

This phase is how JARVIS is allowed near real data. Fully functional still means **you** approve production in V1. Autonomy without this discipline is negligence.

---

## 1. Purpose

Ship the production path:

- Release gate + human approval  
- Immutable frontend/backend deploys with SHA tags  
- Forward-only migrations + rollback **forward**  
- Hardening baked into **every app** JARVIS generates  
- Documentation Agent on successful prod deploy  
- Runbooks for rollback  

Auto-deploy to production for "low risk" changes is **V2+** (`SWE TEAM.MD`). Illegal here.

---

## 2. Non-negotiables

1. **No production deploy while any HIGH or CRITICAL security finding is open.**
2. **No production without human approval** after JARVIS release summary.
3. Database Agent **never** applies migrations by hand to prod. File → pipeline → prod job only.
4. Migrations are **forward-only**. No `DROP COLUMN` / in-place rename / destructive type change as the migrate-forward. Expand-contract only.
5. Every migration file has a corresponding **forward** reverse migration (a new file that undoes, not a down-migration that rewrites history).
6. Deployments are tagged and immutable. Rollback frontend/backend = promote previous artifact. Rollback data = new forward migration.
7. Do **not** auto-rollback the database.
8. Secrets from environment, never committed.
9. Defense in depth: Supabase Auth + RLS on every table + API JWT checks.
10. Fast-track ("skip QC for additive-only schema") is **not** default. If used, only add-column/create-table, never RLS/auth, and it must be explicit in the release summary.
11. Post-deploy watch follows index **C7** (10s / 5 min / 3 consecutive).
12. Each prod ship that passes C8 is recorded — this is the counter Phase 14 will use. Do not invent a second definition later.

---

## 3. Release gate checklist (all true)

- All QA tests green on QC  
- Zero CRITICAL/HIGH security findings  
- Migration dry-run succeeds against production **schema** (no apply)  
- Deploy config validated  
- JARVIS release summary: what changed, what was tested, risk  

**V1:** you approve.  
JARVIS must **block** itself from applying prod without that approval record.

---

## 4. Production deploy sequence

```
Release tag vX.Y.Z
  → Frontend to Vercel production
  → Backend to Railway production
  → Migration against Supabase production
  → Health checks every 10s for 5 minutes
  → Post-deploy smoke
  → Documentation Agent: changelog, API docs from OpenAPI, README if setup changed, runbook if ops changed
  → Record: SHA, timestamp, what changed
```

Order: do not migrate prod before artifacts that need the new schema are deployable, and do not deploy app code that **requires** a migration before the migration is applied — JARVIS's summary must state the order. Prefer **expand** schema first (additive), then code, then later contract.

---

## 5. Database discipline (full law)

| Don't | Do |
|---|---|
| `DROP COLUMN email` | Add `email_v2`, backfill, switch reads, drop later |
| `RENAME users TO members` | New table / dual write / switch / drop later |
| `ALTER COLUMN age TYPE TEXT` | New column, backfill, switch, drop later |

**Conflict prevention:**

1. **Migration lock:** if an open QC candidate includes migrations, new schema changes wait  
2. Timestamp names: `YYYYMMDDHHMMSS_description.sql`  
3. CI: `supabase db push --dry-run` (or equivalent) on PRs that touch migrations  
4. After prod migration, regenerate `database/schema.sql` — agents trust the snapshot, not memory  
5. Any PR touching `migrations/` is reviewed by Database Agent regardless of author  

**Tests:** migration applies, reverse-forward applies, schema matches expected — against throwaway DB in CI.

---

## 6. Rollback procedures

**Frontend (Vercel):** promote previous deployment. Target: seconds.  
**Backend (Railway):** redeploy previous build. Target: ~minutes.  
**Database:** new forward migration. Never "restore the drop."

**Automated rollback (code+frontend/backend)** is V2+. In this phase: **documented manual** (or scripted one-command) rollback. Health watch may **alert** JARVIS; auto-rollback of app tiers can be scripted if it **does not** touch DB — optional, not required. Auto DB rollback remains forbidden.

---

## 7. Hardening the product (every app JARVIS ships)

These are acceptance criteria for coding agents, not blog posts:

| Control | Rule |
|---|---|
| Rate limit | All public routes; token bucket; default 100/min/user; auth 10/min/IP |
| Validation | Pydantic or Zod on every endpoint; 400 with structured error |
| Errors | `code`, `message`, `correlation_id` JSON; no swallowed exceptions |
| AuthZ | RLS every table + API permission checks |
| Health | `/healthz` with version, commit, dependency status; 503 if degraded |
| Feature flags | V1 = env vars only. Unleash is V2+ |
| Frontend perf | Lighthouse CI **job exists**. Targets: Performance > 90, a11y > 95, BP > 95. Misses are Frontend/Design failures in the repair loop, not silent skips. First reference app may miss 90 once if the miss is logged and ticketed. |
| Frontend deps | New dependency > 50KB gzipped needs justification (Code Review). |
| Backend perf | p95 reads < 500ms, writes < 1s measured in QC (record even if not yet blocking) |
| DB | No unjustified full scans on tables expected > 10k rows; Database Agent reviews EXPLAIN for new queries |

Rate limit libs: `slowapi` or `express-rate-limit` (OSS).

---

## 8. Documentation Agent

Runs **after successful production deploy** (not instead of engineering docs during build).

Outputs: CHANGELOG from merged PRs, API docs from OpenAPI, README if setup changed, runbook entries.

Model: Tier 0. Template work.

---

## 9. Out of scope

- Auto-release without human (V2+, after 20+ successful releases)
- Unleash, k6, Grafana
- Operate week (Phase 8)

---

## 10. Exit gate

- [ ] Human approval is a hard blocker in the graph
- [ ] Release summary is generated and stored
- [ ] Prod deploy path works for the reference app (or a staging-prod project if you refuse a public app — still a real prod project, not QC renamed)
- [ ] Migration dry-run against prod schema in the gate
- [ ] Forward-only policy enforced in Database Agent prompt **and** CI checks for banned SQL where feasible
- [ ] Rollback runbook exists and was **executed once** on non-prod or a throwaway prod clone
- [ ] `/healthz` on shipped services
- [ ] Hardening checklist is in coding-agent prompts and Code Review checks
- [ ] Docs agent ran on the successful deploy
- [ ] `schema.sql` regenerated after migrate
- [ ] Deployment table can record a **C8 successful release**
- [ ] Lighthouse CI job exists

---

## 11. Failure modes

| Symptom | Likely cause |
|---|---|
| "Prod" is still QC | Naming lie; fix env |
| Migration applied out of band | Breaks recoverability; treat as incident |
| Human approval is a Slack message with no graph flag | Not a gate |
| Destructive migration merged | Review + CI regex/policy too weak |
| Health 200 while DB down | `/healthz` not checking dependencies |

---

## 12. Time truth

The first production migration will hurt. Budget time for Supabase permissions, RLS mistakes, and DNS. Do not skip the dry-run.
