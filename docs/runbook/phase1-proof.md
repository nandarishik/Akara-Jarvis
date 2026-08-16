# Phase 1 proof of life

## Command

```powershell
.\.venv\Scripts\Activate.ps1
jarvis build "Build a todo API with one authenticated list endpoint"
```

## Record

| | |
|---|---|
| Product path | `projects/<slug>/` |
| Feature branch | `feature/TASK-...` |
| PR | GitHub URL or `docs/reviews/LOCAL_PR-<uuid>.md` |
| Thread id | printed by CLI |
| What failed | |

## Must be true

1. Rows in `intents` / `tasks` on Supabase
2. Worker only wrote `backend/` (plus local PR markdown under `docs/reviews/` if no `gh`)
3. Commit on feature branch
4. `llm_calls` has rows
5. Restarting with the same LangGraph `thread_id` still loads checkpoint (checkpointer wired)
