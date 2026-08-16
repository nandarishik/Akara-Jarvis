# Worker decision (Phase 1)

**Date:** 2026-08-16

**Choice:** `WORKER=fallback` first (scoped file/shell/git ReAct loop). OpenHands is behind the same `Worker` protocol in `src/jarvis/workers/openhands.py` and is **not** the default until Docker/WSL mounts are proven.

**Why:** Constitution allows a thin runner if OpenHands on Windows burns time. Proof of life is a branch/PR, not a perfect OpenHands install.

**OpenHands:** set `WORKER=openhands` after the adapter is implemented. If the Docker mount is empty, the adapter must fail — not report success.

**Kill switch:** Ctrl+C on `jarvis build`; `docker compose --profile offline down` for local Postgres fallback.
