# Akara-Jarvis

Autonomous software engineering system. Phase 1: orchestrator core.

**Law:** [constitutions/PHASE-01-CORE.md](constitutions/PHASE-01-CORE.md)

**GitHub:** https://github.com/nandarishik/Akara-Jarvis

## Virtualenv (required)

```powershell
cd "c:\Users\nanda\OneDrive\Desktop\Akara Team"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -e .
```

Copy `.env.example` to `.env`. Set `OPENROUTER_API_KEY` and `DATABASE_URL`.

`DATABASE_URL` is the **Postgres URI** from Connect → **Direct** or **ORM** (not Framework / Next.js). Use the **session** pooler (`:5432`), not transaction (`:6543?pgbouncer=true`). Replace `[YOUR-PASSWORD]`. Never commit `.env`. Do **not** add Prisma for JARVIS.

## Run

```powershell
.\.venv\Scripts\Activate.ps1
jarvis build "Build a todo API with one authenticated list endpoint"
```

## Hosting

| JARVIS state | Product API | Product UI |
|---|---|---|
| Supabase Postgres | Railway (FastAPI, Phase 3) | Vercel (Phase 3) |
