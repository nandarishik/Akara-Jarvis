# Phase 3 Constitution — Pipeline & Environments

**Duration:** 1–2 days  
**Depends on:** Phase 2 Exit Gate  
**Unlocks:** Phase 4  
**Parent:** [`../SWE TEAM.MD`](../SWE%20TEAM.MD) · Index: [`PHASES.md`](PHASES.md)

This phase is plumbing. Tedious, not clever. The constitution exists so we do not "skip QC" and call localhost production.

---

## 1. Purpose

Make `develop` → DEV → QC a real promotion path. CI must be deterministic. Environments must be named correctly. QA remains a **process**, not an environment.

---

## 2. Non-negotiables

1. **Three environments:** DEV, QC, Production. Production **deploy** is Phase 7; Production **config and accounts** may be created now but auto-deploy to prod is forbidden.
2. QC **mirrors production architecture** (same deploy mechanism, same shape). DEV may be partial.
3. QA Agent tests **QC**, not source (execution of that rule is Phase 4; this phase must give QA a QC URL).
4. Nothing merges to `develop` without lint + types + unit tests + Code Review (from Phase 2).
5. No promotion DEV → QC while CI is red.
6. Secrets never in git. Document names in `docs/environments.md`. Values in platform secret stores.
7. Docker images: **specific tags, never `latest`**. Multi-stage, non-root.
8. Every deployment (even DEV) is traceable to a **git SHA**.
9. CI jobs that are independent **run in parallel** (lint ∥ types ∥ unit; Semgrep ∥ Trivy ∥ Gitleaks).
10. **Gitleaks** is the secret scanner (index **C6**). Pin language/runtime versions in CI (no floating `node:latest`).
11. App **templates** include `GET /healthz` from this phase (even a stub). Phase 7 upgrades it to version + commit + dependency status. Smoke in this phase hits that route (or a documented equivalent if the stub is not deployed yet).

---

## 3. Environment table

| Environment | Purpose | Mirrors production? | Phase 3 duty |
|---|---|---|---|
| DEV | Integration after merge to `develop` | Partial | Deploy on green CI |
| QC | Pre-prod; QA + Security target | Yes | Promote via release-candidate flow |
| Production | Real users | — | Provision only; **no autonomous prod ship** |

Hosting defaults from `SWE TEAM.MD`: Frontend **Vercel**, Backend **Railway**, Database **Supabase**. Alternatives require an ADR.

---

## 4. Stage 0 — already exists (do not regress)

Worker: branch → code → tests → PR → Code Review → merge to `develop`.

Phase 3 **consumes** that merge. It does not replace OpenHands.

---

## 5. Stage 1 — DEV (on merge to `develop`)

GitHub Actions **must** run:

```
Lint + type check
Unit tests
Integration tests (if present)
Build (frontend + backend)
Semgrep (SAST)
Trivy (dependencies)
Secret detection (Gitleaks)
Deploy to DEV (Vercel preview + Railway DEV + Supabase DEV)
Smoke tests against DEV
```

**Gate:** all green before QC promotion.

**CI graph:**

- Parallel: lint, types, unit  
- Parallel: Semgrep, Trivy, Gitleaks  
- Build after lint+types  
- Deploy after build + tests + scans that are required-green  
- Smoke after deploy  

If Semgrep/Trivy are noisy, they still **run**. Fail-on HIGH/CRITICAL as a **release** gate is Phase 4. Phase 3 must **produce artifacts** (SARIF/JSON uploaded). DEV SAST/SCA is not a substitute for QC DAST (ZAP) in Phase 4.

---

## 6. Stage 2 — QC

Promotion creates a **release candidate** and deploys:

- Vercel QC (production-equivalent frontend config)
- Railway QC (production-equivalent backend config)
- Supabase QC (production-equivalent schema, **separate data**)

**Same deploy mechanism as production.** If QC deploy is a special snowflake script, it is unconstitutional.

---

## 7. Promotion logic

```
develop (green DEV)
  → RC branch / tag
  → QC deploy
  → (Phase 4) QA + Security
  → (Phase 7) Release gate + human prod approval
```

Document the exact git refs in `docs/runbook/` (branch names, tag pattern `vX.Y.Z` later).

---

## 8. DevOps Agent outputs (required files)

- Dockerfiles for **agent workers** (multi-stage, non-root, pinned tags)
- `docker-compose.yml` for local JARVIS + Postgres + worker (Phase 1 may have a draft; Phase 3 hardens it)
- `.github/workflows/` as above
- `docs/environments.md` — variable **names**, not values
- Health check: product templates include `GET /healthz` (full JSON body is Phase 7; JARVIS platform health is Phase 5)

---

## 9. Smoke tests (Phase 3)

Smoke ≠ Playwright E2E.

Smoke **must**:

- Hit `/healthz` on DEV after deploy (stub 200 is enough in this phase)
- Fail the workflow if deploy is unreachable

That is sufficient. Full journeys are Phase 4.

---

## 10. Out of scope

- Playwright suites, ZAP DAST, repair loop (Phase 4)
- Human prod button + migration dry-run against prod (Phase 7)
- Grafana, k6, Unleash
- Auto-merge of RC to production

---

## 11. Exit gate

- [ ] `docs/environments.md` exists
- [ ] GitHub Actions on `develop`: lint, types, tests, build, Semgrep, Trivy, Gitleaks
- [ ] Independent jobs parallelized
- [ ] DEV deploys on green and smoke test runs
- [ ] QC can be deployed with production-equivalent mechanism
- [ ] Secrets not in repo (verified by Gitleaks on a clean tree)
- [ ] Worker Dockerfiles pinned, non-root
- [ ] SHA is visible on the deployed DEV revision
- [ ] Runtime versions pinned in CI
- [ ] Product templates include `/healthz`

---

## 12. Failure modes

| Symptom | Likely cause |
|---|---|
| CI green locally, red in Actions | Missing env / Node/Python version drift — pin versions |
| Preview URL 404 | Wrong Vercel project / root directory in monorepo |
| Railway can't find backend | Root path / start command |
| Secrets scan fails on fixtures | Add allowlist **only** for fake secrets, documented |
| QC "works" via laptop localhost | You did not deploy QC; unconstitutional |

---

## 13. Time truth

YAML is fast. Three cloud dashboards are slow. Do not skip QC "until later" — Phase 4 has nowhere to point Playwright.
