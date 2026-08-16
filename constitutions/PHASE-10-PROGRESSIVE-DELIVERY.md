# Phase 10 Constitution — Progressive Delivery (V2)

**Track:** Full potential (V2+)  
**Depends on:** Phase 8 Exit Gate; Phase 7 production path  
**Unlocks:** canaries, instant disable, auto app-tier rollback  
**Parent:** [`../SWE TEAM.MD`](../SWE%20TEAM.MD) §9 Unleash, §13 Automated Rollback · Index: [`PHASES.md`](PHASES.md)

---

## 0. Trigger (start only if true)

**Unleash / flags:** you need canary releases or gradual rollouts. V1 ships all-or-nothing; env-var flags are no longer enough.

**Automated rollback:** deployment frequency is high enough that **manual** rollback is too slow (the doc's bar: not "we deploy weekly").

Either sub-trigger may fire alone. If you auto-rollback without flags, you still cannot dark-launch. If you have flags without auto-rollback, you can disable a feature but a crash-looping release still needs a human.

**Do not start** to make the architecture diagram prettier.

---

## 1. Purpose

Replace env-var flags with self-hosted [Unleash](https://github.com/Unleash/unleash) (Apache 2.0):

- Ship code to production **without activating** it
- Canary: **5% → 25% → 100%**
- Instant deactivation without redeploy

Install **automated rollback** for frontend (Vercel) and backend (Railway) when post-deploy health fails **3 consecutive** times (index **C7**: every 10s for 5 minutes):

1. Auto-rollback frontend and backend  
2. **Do NOT** auto-rollback the database  
3. Notify JARVIS → investigate → fix → redeploy through the **normal** pipeline (review, DEV, QC, QA)

---

## 2. Non-negotiables

1. Unleash is **self-hosted**. No Unleash Cloud as the long-term law (trial to learn is not an exception that stays in prod).
2. Every product JARVIS ships in this era uses Unleash (or a documented compatible OSS flags SDK), not a new flags invention.
3. Flags default **off** for new features until canary starts.
4. Auth, payments, and data-deletion paths must not be "flagged on for 5%" in a way that corrupts data for that 5%. Prefer flags that are **behavior** not **schema**.
5. Schema/migrations still forward-only. A flag does not justify a destructive migration.
6. Auto-rollback **never** applies a down-migration or restore-over-prod.
7. Auto-rollback is **idempotent**. Triple-firing health must not yo-yo deploys forever — circuit: rollback once, then escalate.
8. After rollback, JARVIS opens a fix task with health logs, SHA, and release summary. Max 3 repair attempts still apply.
9. Human can freeze rollouts (`jarvis freeze-release`).

---

## 3. Canary law

```
QC pass + (human or later auto-release)
  → prod at 5% (flag or platform split)
  → watch error rate / health
  → 25% → 100%
```

If 5% or 25% breaches alert rules (Phase 11 if present; otherwise health + 5xx): **halt ramp**, disable flag or rollback app tier, do not continue to 100%.

---

## 4. In scope

- Unleash deploy + SDKs in frontend/backend templates Design/Frontend/Backend agents must use
- Canary runbook and JARVIS tasks for ramp
- Scripts: `vercel rollback` / Railway previous build, triggered by health watcher
- Audit: who/what flipped a flag, SHA, timestamp

---

## 5. Out of scope

- Auto-release without human (Phase 14; needs 20+ successful releases)
- Grafana-full (Phase 11) — health watcher from Phase 7/8 is enough to *trigger* rollback; richer alerts come with Phase 11
- Temporal (Phase 12) — canary timers may stay in JARVIS/Postgres until Temporal exists
- k6 (Phase 13)

---

## 6. Exit gate

- [ ] Trigger recorded  
- [ ] Unleash running; one feature shipped dark then enabled  
- [ ] 5/25/100 ramp documented and executed once on a real feature  
- [ ] Instant disable without redeploy proven  
- [ ] Staged health-fail drill: 3 consecutive failures → app rollback, DB untouched  
- [ ] No yo-yo (second rollback suppressed; DLQ/escalation)  
- [ ] Coding-agent prompts require flags for new user-facing features  
- [ ] `docs/runbook/progressive-delivery.md`

---

## 7. Failure modes

| Symptom | Likely cause |
|---|---|
| Canary 5% still hits everyone | Flag not in the request path; cached HTML |
| DB migrated, app rolled back, app old + schema new | Expected if additive; **illegal** if rollback needed old columns you dropped |
| Rollback loop | Health check wrong; check `/healthz` deps |
| Unleash down, all flags fail closed/open badly | Document fail-closed for risky features |
