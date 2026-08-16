# Phase 13 Constitution — Performance & Scale (V2)

**Track:** Full potential (V2+)  
**Depends on:** Phase 8 Exit Gate; **traffic baselines** for k6; **measured** DB bottleneck for Redis  
**Unlocks:** load tests in QC; Redis when Postgres is the proven hot path  
**Parent:** [`../SWE TEAM.MD`](../SWE%20TEAM.MD) §9 Performance, §15 k6 + Redis · Index: [`PHASES.md`](PHASES.md)

---

## 0. Triggers (independent)

| Work | Trigger | Why wait |
|---|---|---|
| **k6** | You have **traffic baselines** to test against | Pointless without real patterns |
| **Redis** | Database queries are a **measurable** bottleneck | In-memory LRU is enough for V1 |

**Do not start** k6 with invented RPS. **Do not start** Redis because every tutorial has a cache.

---

## 1. Purpose

**k6** ([AGPL-3.0](https://github.com/grafana/k6)): load test QC (and later prod-like) using recorded or observed patterns — not fantasy scale.

**Redis:** cache only the hot paths EXPLAIN/metrics proved. Not a second database, not a session store "because," not a message queue unless ADR'd (prefer not — Temporal/Postgres already exist).

Keep existing budgets from Phase 7:

- Frontend Lighthouse: Performance > 90, a11y > 95, BP > 95  
- Backend: p95 reads < 500ms, writes < 1s in QC  
- No full table scans on tables expected > 10k rows  

This phase **enforces** those with load, not only unit-time measurements.

---

## 2. Non-negotiables

1. k6 scripts live in git (`tests/load/`). They are artifacts QA/DevOps own.
2. Load tests run against **QC**, never as a surprise against production, unless an ADR allows a carefully rate-limited prod probe.
3. Baselines committed: p50/p95/p99, error rate, from real or staging-prod metrics (Phase 11 if present).
4. A load test that fails the budget **blocks** the same way QA fails — repair loop, max 3, responsible agent (often Backend/Database).
5. Redis is OSS, pinned image tags, auth on, not exposed to the public internet.
6. Cache keys include version/SHA or schema generation so deploys do not serve poison forever.
7. Cache-aside; DB remains source of truth. Forward-only migrations still apply.
8. RLS/authz is not bypassed via cache (never cache another user's private row under a global key).
9. LRU in-process remains allowed for tiny hot data; Redis is for **shared** multi-instance bottlenecks.

---

## 3. In scope

- k6 in CI on QC promote (or nightly if too slow for every PR — document which)  
- Database Agent: EXPLAIN on new queries still required; k6 is the proof under load  
- Redis only after a named query/endpoint is shown hot in metrics  
- Runbook: `docs/runbook/load-and-cache.md`  

---

## 4. Out of scope

- Kubernetes autoscaling theatre without traffic  
- Replacing Postgres  
- CDN as a substitute for fixing N+1 (CDN is fine as extra; not this phase's law)  
- Forgejo, Temporal, Unleash unless already triggered elsewhere  

---

## 5. Exit gate

**k6 (if triggered):**

- [ ] Baseline file exists (source of numbers cited)  
- [ ] k6 scenario matches that mix (read/write/auth)  
- [ ] QC run is automated; fail budget → JARVIS repair path  
- [ ] At least one failure was real and fixed (or a drill)

**Redis (if triggered):**

- [ ] Bottleneck query/endpoint named with metric evidence  
- [ ] Cache hit/miss metrics exist  
- [ ] Authz-safe keys proven with a test (user A must not get user B)  
- [ ] Invalidation on deploy/migration documented  

---

## 6. Failure modes

| Symptom | Likely cause |
|---|---|
| k6 green, users still unhappy | Wrong baseline; testing the health endpoint |
| Redis "fixes" prod, QC empty | No cache in QC; environments must match mechanism |
| User B sees user A data | Cached GraphQL/REST without user in key |
| Load test is a DDoS | Aimed at prod; constitution breach |
