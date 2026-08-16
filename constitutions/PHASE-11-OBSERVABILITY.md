# Phase 11 Constitution — Observability & Autonomous Incidents (V2)

**Track:** Full potential (V2+)  
**Depends on:** Phase 8 Exit Gate; real production traffic (or a hard need for dashboards/alerting)  
**Unlocks:** JARVIS investigates alerts and opens fixes; you review the PR, not the pager noise  
**Parent:** [`../SWE TEAM.MD`](../SWE%20TEAM.MD) §10 V2+ · Index: [`PHASES.md`](PHASES.md)

---

## 0. Trigger (start only if true)

**Grafana + Prometheus + Loki:** you need real-time dashboards or automated alerting. Structured logs + health checks are no longer enough.

**Sentry:** production runs **continuously with real users**. Logs are not enough to group crashes.

**Do not start** with zero users "so we're ready." This stack is operational burden.

---

## 1. Purpose

Install the V2 observability plane (all OSS / self-hostable):

| Component | Tool | License | Purpose |
|---|---|---|---|
| Collection | OpenTelemetry Collector | Apache 2.0 | Traces, metrics, logs in |
| Metrics | Prometheus | Apache 2.0 | Time series |
| Dashboards | Grafana | AGPL-3.0 | Visualize + alert |
| Logs | Loki | AGPL-3.0 | Log aggregation |
| Traces | Jaeger | Apache 2.0 | Distributed tracing |
| Errors | Sentry self-hosted | FSL | Grouping + alerting |

**V2 goal (binding):** JARVIS **receives** these alerts, reads logs/traces, identifies a likely cause, writes a fix, pushes it through the **normal pipeline**. You review the **fix**, not the raw alert.

---

## 2. Non-negotiables

1. Open source / self-hosted as tabled. No Datadog/New Relic as the constitution (hosting exceptions in global law do not include APM SaaS).
2. Every service JARVIS **is** and every app it **ships** emits OTel (**trace id = `correlation_id`** from Phase 5).
3. Grafana alert rules from the spec are **mandatory**:
   - 5xx rate > 1% over 5 minutes  
   - p95 response time > 2s over 5 minutes  
   - Health check failure > 2 consecutive  
   - Database connection pool > 80% utilized  
4. Alerts page JARVIS with: alert name, labels, time, links to Grafana/Loki/Jaeger/Sentry, SHA, env.
5. JARVIS incident tasks are **critical**: they **do not pause** for daily LLM budget (Phase 2 budget law: production fixes continue).
6. Fixes still go through Code Review, DEV, QC, QA. Observability is not a license to SSH-hotfix prod.
7. Auto-rollback (if Phase 10 is live) may run **first**; investigation still happens.
8. No PII in traces/logs beyond what the product already stores. Redact secrets. Sentry scrubbing on.
9. V1 JSON logs remain. Loki **ingests** them; do not invent a second incompatible log format.

---

## 3. Autonomous investigate loop

```
Alert → JARVIS incident task (critical)
  → retrieve logs/traces/errors for correlation_id / SHA
  → hypothesize + patch via responsible agent
  → Code Review → DEV → QC → QA
  → human reviews the PR/release (until Phase 14 low-risk auto)
  → if cannot locate cause in 3 attempts → dead letter with evidence pack
```

The evidence pack: alert JSON, log excerpts, trace ids, suspected files, what was tried.

---

## 4. In scope

- OTel SDKs in frontend/backend **templates** so new JARVIS apps are born instrumented
- Dashboards: RED (rate, errors, duration), deploy annotations (SHA)
- Sentry project per environment
- Alert routing into JARVIS API
- Runbook: `docs/runbook/observability.md`

---

## 5. Out of scope

- k6 (Phase 13) — may **consume** metrics later  
- Temporal (Phase 12)  
- Replacing `/healthz`  
- Auto-release (Phase 14)  

---

## 6. Exit gate

- [ ] Trigger recorded (traffic or continuous users)  
- [ ] All six components up; one Grafana folder for JARVIS + one for a shipped app  
- [ ] Four alert rules fire in a **drill** (can be synthetic)  
- [ ] Drill: alert → JARVIS task → PR with a real (or staged) fix path  
- [ ] correlation_id visible in Loki and Jaeger for one request  
- [ ] Sentry groups a deliberate error  
- [ ] Budget pause does **not** drop incident tasks  
- [ ] 3 failed investigates → DLQ with evidence pack  

---

## 7. Failure modes

| Symptom | Likely cause |
|---|---|
| Alert storms | Thresholds too tight; tune, don't disable |
| JARVIS patches the wrong service | Missing deploy annotations / wrong SHA |
| Trace broken at frontend | OTel not in browser or missing propagator |
| Sentry is a junk drawer | No scrubbing, no release version |
| Investigate loops forever | Treat like QA: max 3 |
