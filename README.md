# JARVIS

Autonomous software engineering system. Phase 1: orchestrator core.

**Law:** [constitutions/PHASE-01-CORE.md](constitutions/PHASE-01-CORE.md)

## Virtualenv (required)

```powershell
cd "c:\Users\nanda\OneDrive\Desktop\Akara Team"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -e .
```

Copy `.env.example` to `.env`. Set `OPENROUTER_API_KEY` and `DATABASE_URL` (Supabase → Settings → Database → URI). Never commit `.env`.

## Run

```powershell
.\.venv\Scripts\Activate.ps1
jarvis build "Build a todo API with one authenticated list endpoint"
```

## Hosting

| JARVIS state | Product API | Product UI |
|---|---|---|
| Supabase Postgres | Railway (FastAPI, Phase 3) | Vercel (Phase 3) |

## GitHub

https://github.com/nandarishik/akara-jarvis
