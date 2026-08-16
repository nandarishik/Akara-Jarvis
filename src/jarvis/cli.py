from __future__ import annotations

import signal
from contextlib import nullcontext
from pathlib import Path
from uuid import uuid4

import typer
from dotenv import load_dotenv
from langgraph.checkpoint.postgres import PostgresSaver

from jarvis.config import get_settings
from jarvis.db import store
from jarvis.graph import compile_app
from jarvis.scaffold import ensure_template

load_dotenv()

app = typer.Typer(add_completion=False, no_args_is_help=True)


def _shutdown(*_args) -> None:
    raise SystemExit(130)


def _install_signals() -> None:
    signal.signal(signal.SIGINT, _shutdown)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, _shutdown)


def _checkpoint_cm(database_url: str):
    if not database_url:
        return nullcontext(None)
    url = database_url
    if "sslmode" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}sslmode=require"
    return PostgresSaver.from_conn_string(url)


@app.command()
def build(intent: str = typer.Argument(..., help="What to build")) -> None:
    """Phase 1 stub CLI: one backend worker, branch + PR."""
    _install_signals()
    settings = get_settings()
    if not settings.openrouter_api_key:
        typer.echo("OPENROUTER_API_KEY missing in .env", err=True)
        raise typer.Exit(1)
    if not settings.database_url:
        typer.echo(
            "DATABASE_URL missing. Supabase → Settings → Database → URI.",
            err=True,
        )
        raise typer.Exit(1)
    conn = store.connect(settings.database_url)
    try:
        store.apply_schema(conn)
        with _checkpoint_cm(settings.database_url) as saver:
            if saver is not None:
                saver.setup()
            graph = compile_app(settings, conn, saver)
            thread_id = str(uuid4())
            result = graph.invoke(
                {"intent": intent},
                {"configurable": {"thread_id": thread_id}},
            )
            typer.echo(result.get("result") or result)
            typer.echo(f"product={result.get('product_root')} thread={thread_id}")
    finally:
        conn.close()


@app.command("init-template")
def init_template() -> None:
    settings = get_settings()
    ensure_template(Path(settings.jarvis_projects_root) / "_template")
    typer.echo("template ready")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
