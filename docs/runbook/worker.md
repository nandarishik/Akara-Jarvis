# Worker decision (Phase 1)

**Date:** 2026-08-17 (updated)

**Default:** `WORKER=openhands` — real [OpenHands Software Agent SDK](https://docs.openhands.dev/sdk/guides/agent-server/overview).

| Docker Desktop engine | What runs |
|---|---|
| Up (`docker info` succeeds) | `DockerWorkspace` + `ghcr.io/openhands/agent-server:latest-python` |
| Down | OpenHands **local** workspace on the product dir — still OpenHands, not the thin ReAct fallback |

**Model:** OpenHands uses the agent entry from `config/model-routing.yaml` (`openhands_settings.model`), typically `openrouter/minimax/minimax-m3` for backend. See [`models.md`](models.md).

**Fallback** (`WORKER=fallback`) stays for emergencies if the SDK is unavailable; it also resolves models via the Portfolio B router.

**Why it was fallback before:** proof of life shipped before OpenHands was wired, because Docker Desktop was not running. The constitution allows that. It does not require staying on fallback forever.

**Start Docker Desktop** if you want the isolated container path. Until then, local OpenHands is the working path.

**Kill switch:** Ctrl+C on `jarvis build`. Stop Docker Desktop to stop containers.
