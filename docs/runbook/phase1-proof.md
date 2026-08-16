# Phase 1 proof of life

## Command

```powershell
.\.venv\Scripts\Activate.ps1
jarvis build "Build a todo API with one authenticated list endpoint"
```

## Record (2026-08-16)

| | |
|---|---|
| Product path | `projects/build-a-todo-api-with-one-authenticated/` |
| Feature branch | see product git (`feature/TASK-0ffe8f96-...`) |
| PR | `docs/reviews/LOCAL_PR-0ffe8f96-ed65-44b2-86e3-32506915cea6.md` (no `gh` CLI) |
| Thread id | `27560cb2-2a16-42a1-8d0f-70facae9aa37` |
| Task id | `0ffe8f96-ed65-44b2-86e3-32506915cea6` |
| Status | completed |
| Tokens | 1640 |
| What failed | Nothing on this run. Auth on `/todos` was not implemented (in-memory list only). GitHub repo still not created (`gh` missing). |

## Must be true

1. Rows in `intents` / `tasks` on Supabase
2. Worker only wrote `backend/` (plus local PR markdown under `docs/reviews/` if no `gh`)
3. Commit on feature branch
4. `llm_calls` has rows
5. Restarting with the same LangGraph `thread_id` still loads checkpoint (checkpointer wired)
