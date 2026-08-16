# Phase 14 Constitution — Sovereign Ops & Auto-Release (V2)

**Track:** Full potential (V2+) — last phase in the vision doc  
**Depends on:** Phase 8 Exit Gate; **20+ successful production releases** before auto-release; Forgejo only if self-host CI is a **hard** requirement  
**Unlocks:** GitHub-optional CI; low-risk auto-prod; the "full potential" operate mode  
**Parent:** [`../SWE TEAM.MD`](../SWE%20TEAM.MD) §6 V2 auto-release, §15 Forgejo + Woodpecker + auto-release · Index: [`PHASES.md`](PHASES.md)

---

## 0. Triggers (independent; do not bundle casually)

| Work | Trigger |
|---|---|
| **Auto-release** | QA pipeline proven over **20+ successful releases**. Trust is earned. |
| **Forgejo + Woodpecker** | "Everything self-hosted" is a **hard requirement**. GitHub Actions is more productive until then. |

You may auto-release **on GitHub Actions**. You may move CI to Forgejo **without** auto-release. Doing both at once without a trigger for each is a constitutional violation.

**Do not start** auto-release on release #3 because the demo went well.

---

## 1. Purpose

1. **V2 release policy:** low-risk releases (no schema changes, no auth changes, **only additive features**) may auto-deploy after QC + QA + Security pass. **High-risk still requires human approval.**
2. Optional sovereign CI: Forgejo + Woodpecker (or documented OSS pair) replacing GitHub Actions **when** the trigger fires.
3. Full-potential loop: alert (Phase 11) or `jarvis build` → pipeline → **auto-prod if low-risk** → canary (Phase 10) → watch → rollback if needed.

---

## 2. Non-negotiables

1. **High-risk = human:** schema/migrations, auth, RLS, payments, data deletion, security HIGH/CRITICAL just closed, anything touching `database/migrations/`.
2. **Low-risk definition is code**, not a vibe. JARVIS classifies the RC (paths, OpenAPI diff, migration presence). If uncertain → human.
3. Auto-release still requires: QA green, zero CRITICAL/HIGH, health, SHA record, Documentation Agent.
4. Auto-release **does not** skip Code Review.
5. 20+ **C8 successful production releases** in the deployment table — not previews.
6. Forgejo/Woodpecker must reproduce Phase 3 CI: lint, types, tests, build, Semgrep, Trivy, Gitleaks, parallel independent jobs. Weaker CI to leave GitHub is illegal.
7. Secrets move to the new CI secret store; Gitleaks still runs.
8. Open source or don't use it. Hosting exceptions remain Vercel/Railway/Supabase unless you ADR off them (not required for this phase).
9. If you auto-release many times per day, Phase 10 rollback trigger is met — **install rollback before** high-frequency auto-prod.
10. You can **disable** auto-release in one switch. Default after incidents: off.

---

## 3. In scope

- Risk classifier + audit log of why a release was auto vs human
- Deployment counter + "20 successful" on the dashboard
- Woodpecker/Forgejo pipeline parity with GitHub
- Mirror or migrate repos; preserve SHA traceability
- Runbook: break-glass human approve, disable auto-release, GitHub fallback if Forgejo dies

---

## 4. Out of scope

- Training custom models
- Dropping Vercel/Railway/Supabase without a separate ADR
- Auto-release of first-time products JARVIS has never shipped
- Weakening ZAP/Semgrep to make auto-release greener

---

## 5. What "full potential" means after this phase

Combined with Phases 1–13 (as their triggers allowed):

You describe a product. JARVIS plans, codes, reviews, tests, scans, canaries, load-tests if baselines exist, observes, and **ships low-risk changes without you**. High-risk still stops for you. Incidents become PRs. Tier 0 can run on your electricity. CI can live on your metal. The database is still forward-only. The UI is still not slop.

That is the end of `SWE TEAM.MD` as written. Anything past this is a new constitution.

---

## 6. Exit gate

**Auto-release (if that trigger fired):**

- [ ] ≥ 20 **C8** successful prod releases recorded
- [ ] Classifier tested: migration PR → human; docs-only/additive UI → auto
- [ ] One auto-release to prod with full QC/QA/Security
- [ ] Kill switch demonstrated
- [ ] Audit log can explain a bad ship

**Sovereign CI (if that trigger fired):**

- [ ] Forgejo + Woodpecker (or ADR'd OSS pair) run the full Phase 3+4 CI
- [ ] GitHub no longer required for the happy path
- [ ] Fallback documented
- [ ] Worker images still pinned, non-root

**Both:** `docs/runbook/auto-release.md` and/or `docs/runbook/sovereign-ci.md`

---

## 7. Failure modes

| Symptom | Likely cause |
|---|---|
| Migration auto-shipped | Classifier used PR title not file paths |
| Counted preview deploys as 20 | Wrong table |
| CI green, weaker scans | Woodpecker port skipped ZAP/Gitleaks |
| Cannot stop the machine | Kill switch not wired to scheduler |
| Two CIs diverged | No single pipeline definition |

---

## 8. Time truth

This phase is mostly **policy and proof**, not new agents. The 20 releases are the schedule. Forgejo is a migration project — treat it as a week of plumbing, not an afternoon of YAML.
