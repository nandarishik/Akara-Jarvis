# Phase 6 Constitution — Intelligence & Control

**Duration:** 3–5 days  
**Depends on:** Phase 5 Exit Gate  
**Unlocks:** Phase 7  
**Parent:** [`../SWE TEAM.MD`](../SWE%20TEAM.MD) · Index: [`PHASES.md`](PHASES.md)

This phase turns a pipeline into a **product you operate** and agents that **see the codebase**. It also enforces the anti-slop law with evidence, not slogans.

---

## 1. Purpose

1. **Codebase intelligence:** chunk → embed → pgvector; incremental index; retrieval into the context package  
2. **Control plane:** `jarvis` CLI/daemon, workspace sandbox, kill switch, dashboard for graph / spend / dead letters  
3. **Design verification:** Design Agent (or a designated check) compares QC screenshots to spec; slop fails the loop  

---

## 2. Non-negotiables

1. Agents must not receive "the entire repo" as the default context. Retrieval is mandatory once the project exceeds the point where dumping works — **and we install RAG now** so Sept 16 apps don't rot.
2. Embedding model: free/near-free via OpenRouter **or** self-hosted Sentence Transformers. No proprietary-only embedding lock-in.
3. Vector store: **pgvector** (Supabase/Postgres). Do not add a second vector DB.
4. Index: full index on project init; **incremental re-index on merge to `develop`** (changed files only).
5. Dedup: if two agents need the same artifact/context, fetch once, share.
6. Response cache: if global files unchanged, do not re-embed/re-summarize blindly.
7. JARVIS **control** is scoped to `projects/{name}/` (or documented workspace root). Host-wide admin remains forbidden.
8. Kill switch stops orchestrator and workers.
9. **No AI-slop UI** is now a **gate**, not a prompt paragraph. If QC screenshots match banned patterns, send back to Design, then Frontend — not a warning in a log nobody reads.
10. Dashboard/CLI for JARVIS itself must also obey anti-slop (shadcn/Radix/ReactBits etc.). JARVIS looking like a generic AI admin panel is a fail.

---

## 3. RAG law

```
Source files → chunk by function/class → embed → pgvector
```

On task start, query vector store from the task description. Results go into context package slot **Relevant code**.

**Do not remove** the always-on files from Phase 5. RAG **adds**, it does not replace contracts/schema/ADRs/tokens.

If retrieval returns nothing useful, JARVIS still includes always-on files and path-based fallback. Empty RAG ≠ empty context.

---

## 4. Control plane law

**Minimum CLI:**

```text
jarvis start
jarvis stop
jarvis build "<intent>"
jarvis build --from-file idea.md
jarvis status
jarvis spend
jarvis dead-letter
jarvis resume --task <id> --note "..."
```

Phase 1 may have shipped a stub `build`. This phase completes the control plane. `resume` is required so Phase 8's DLQ UX is not fiction.

**Daemon:** can run as a long-lived process (compose or service). `start` brings up Postgres + orchestrator + worker runtime.

**Dashboard (V1):**

- Task DAG (id, agent, status, retries, tokens)
- Current spend vs budget
- Dead letter list with expand-for-context
- Kill / pause agent
- Link to PRs / QC URL

No requirement for realtime collaborative multiplayer. Requirement: you can **see and stop** the system without reading Postgres by hand.

---

## 5. Anti-slop verification

Design Agent outputs still include library selection and tokens.

**New in Phase 6:** Playwright screenshots of QC (from Phase 4 artifacts or a dedicated capture) are attached to a Design verification step.

**Fail if:**

- Banned layout tropes dominate the primary views
- Spec named a library and the implementation clearly did not use it
- No motion where the spec required Framer Motion / ReactBits

This check uses eyes (screenshots + spec), not "LLM, is this pretty?" as the only signal. An LLM may **assist** comparison; it may not replace the spec's library list.

---

## 6. Prompt caching

Role prompts are stable. Use OpenRouter prompt caching. This is cost control from `SWE TEAM.MD` §8 and belongs here once the control plane tracks spend visibly.

---

## 7. Out of scope

- Production migration dry-run, human release ritual (Phase 7)
- Week of multi-app operate (Phase 8)
- Temporal, Grafana, Ollama — V2 constitutions 9–14; **no** "OpenRouter is down so we install Ollama this afternoon" exception. Use Phase 9's trigger.

---

## 8. Exit gate

- [ ] pgvector index builds on init and updates on `develop` merge
- [ ] Coding agents receive retrieved chunks + always-on files
- [ ] CLI: start/stop/build/status/spend/dead-letter/**resume** work
- [ ] Dashboard or TUI shows graph + spend + DLQ
- [ ] Kill switch stops workers
- [ ] Workspace sandbox enforced
- [ ] At least one UI fail from anti-slop check was caught and sent back (can be staged)
- [ ] JARVIS's own UI is not generic-AI-slop

---

## 9. Failure modes

| Symptom | Likely cause |
|---|---|
| Agents still invent files that exist | Chunking too coarse / query not using task verbs |
| Stale retrieval | No incremental index |
| Dashboard pretty, build broken | Control plane must not regress Phase 1 loop |
| Anti-slop never fails | Check is a no-op; add a known-bad fixture |
| Embeddings expensive | Wrong model; switch to cheap/self-hosted |

---

## 10. Time truth

RAG and the control plane are each a real project. Cut dashboard **visual** scope before you cut retrieval or kill switch. A boring CLI that is true beats a lying UI.
