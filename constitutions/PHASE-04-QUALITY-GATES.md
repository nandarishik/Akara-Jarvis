# Phase 4 Constitution — Quality Gates

**Duration:** 1–2 days  
**Depends on:** Phase 3 Exit Gate (QC URL exists)  
**Unlocks:** Phase 5  
**Parent:** [`../SWE TEAM.MD`](../SWE%20TEAM.MD) · Index: [`PHASES.md`](PHASES.md)

This phase is where JARVIS earns the right to say "tested" and "scanned." Tools do the work. Agents interpret. The repair loop becomes real.

---

## 1. Purpose

Against **QC**, in parallel:

- QA Agent exercises the **running app** (Playwright)
- Security Agent runs **Semgrep + Trivy + ZAP**, consolidates findings

On fail: JARVIS identifies the responsible agent, attaches test/scan output + code + original spec, retries through Code Review → DEV → QC → QA again. **Max 3.**

On pass: candidate is eligible for the Release Gate (Phase 7). Phase 4 does not deploy production.

---

## 2. Non-negotiables

1. QA **does not review source** to decide pass/fail. It drives a browser / hits HTTP like a user.
2. Security **does not** "ask an LLM if this is secure." It runs Semgrep CE, Trivy, OWASP ZAP.
3. Authoring agent cannot close a QA/Security fail by arguing. Only a new reviewed change can.
4. Tests are **deterministic**. No `sleep` for timing. Playwright `waitFor` patterns. Tests create and clean their own data.
5. Testing pyramid: QA owns **E2E critical journeys only**. Unit/integration stay with coding agents. Do not invert the pyramid.
6. Blocking security: **CRITICAL and HIGH block** promotion. MEDIUM = flagged. LOW/INFO = logged.
7. ZAP **runs** in this phase. If too flaky to **block**, a written exception is required: what is ignored, **why**, and an **expiry** (must be revisited by Phase 8 Exit Gate). Semgrep + Trivy HIGH/CRITICAL **always** block. Silent skip of all DAST is unconstitutional.
8. Repair loop uses Phase 1–2 machinery. This phase only **connects real report JSON** into it. Retries use **issue_key** (index **C4**). If the test matches a **bad spec**, route Product (or Architect), not only Frontend.

---

## 3. QA Agent law

**Stack:** Playwright (Apache 2.0)  
**Target:** QC  
**Model:** Tier 0 for scripts from specs; Tier 2 only for new test strategy

**Must cover (when the product has the feature):**

- Critical journey (signup → onboard → core action → result)
- Form validation
- Auth (login, logout, session expiry, password reset if present)
- Authorization (user A must not see user B's data)
- Chromium + Firefox + WebKit
- Mobile viewport **375px** minimum
- Error states (API down, bad input)
- Persistence (create, refresh, still there)

**Generation rule:** scripts come from Product Given/When/Then, not from vibes.

**Report schema (mandatory):**

```json
{
  "agent": "qa",
  "status": "passed | failed",
  "target": "qc",
  "journeys": [{ "name": "string", "result": "passed | failed", "error": null }],
  "artifacts": ["path to trace/video/screenshot"],
  "responsible_hint": "frontend | backend | database | unknown"
}
```

---

## 4. Security Agent law

| Tool | Job |
|---|---|
| Semgrep CE | SAST — injection, XSS, crypto, secrets patterns |
| Trivy | SCA, image, IaC misconfig |
| OWASP ZAP | DAST against running QC |

All three **in parallel**. Agent deduplicates, assigns severity, emits one report to JARVIS.

**Consolidated report schema:**

```json
{
  "agent": "security",
  "status": "passed | blocked | review",
  "findings": [{
    "id": "string",
    "tool": "semgrep | trivy | zap",
    "severity": "CRITICAL | HIGH | MEDIUM | LOW | INFO",
    "title": "string",
    "location": "string",
    "evidence": "string"
  }],
  "blockers": []
}
```

`blocked` if any CRITICAL or HIGH remains open.

LLM job: parse tool JSON/SARIF into this schema. **Not** to invent vulnerabilities.

---

## 5. Combined gate

```
QC ready
  ├── QA Playwright (browsers + mobile)
  ├── API contract tests (valid + invalid) — QA or Backend-owned contract suite run here
  ├── Semgrep
  ├── Trivy
  └── ZAP
        ↓
Combined report → JARVIS
```

**FAIL:** route to responsible agent; include failing output + relevant code + original spec. Fix → Code Review → merge → DEV → QC → re-run. Same **issue_key**, max 3.

**PASS:** release candidate waits at Phase 7 gate.

If responsibility is `unknown`, JARVIS assigns Architect or the last touching agent — never drops the fail.

---

## 6. API contract tests

Every endpoint: valid and invalid inputs. These may live with Backend but **must execute** in the QA gate against QC, not only in unit tests.

Frontend/Backend drift is a Quality Gate failure, not a "we'll notice in prod" issue.

---

## 7. Out of scope

- Production deploy, migration dry-run vs prod (Phase 7)
- Crash recovery drills (Phase 5)
- Visual anti-slop screenshot loop (Phase 6) — QA may capture screenshots as artifacts; Design verdict is Phase 6
- k6 load tests (V2+)

---

## 8. Exit gate

- [ ] Playwright runs against QC from Given/When/Then for the reference app
- [ ] Tests are deterministic on a clean QC (documented how data is seeded)
- [ ] Semgrep + Trivy + ZAP run; consolidated JSON exists
- [ ] HIGH/CRITICAL block the candidate
- [ ] One **intentional** fail (broken assertion or known finding) proves: JARVIS creates a fix task, Code Review runs, pipeline re-enters
- [ ] Third failure on the same **issue_key** dead-letters instead of looping
- [ ] ZAP either blocks on HIGH/CRITICAL or has an expiry-dated exception
- [ ] Bad-spec path: at least documented (Product/Architect can be assigned)
- [ ] Parallelism: QA and Security start together, not sequentially unless a hard dependency exists (ZAP needs QC up — QC up is the only wait)

---

## 9. Failure modes

| Symptom | Likely cause |
|---|---|
| Flaky E2E | `sleep`, shared data, no waitFor |
| ZAP 400 findings | Unauthenticated spider + missing ignore; tune, don't disable |
| Repair loops the wrong agent | Report missing `responsible_hint` / JARVIS routing weak |
| Infinite QA fail | Spec is wrong; Product must be in the retry path when tests match a bad spec |
| Gate skipped "because QC was down" | Phase 3 regression; stop Phase 4 until QC is up |

---

## 10. Time truth

Playwright generation is easy. Determinism is the work. ZAP is the schedule risk. Do not let ZAP eat the repair-loop integration — wire Semgrep/Trivy + Playwright first, then ZAP, still in this phase.
