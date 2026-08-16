from __future__ import annotations

import re
import shutil
from pathlib import Path

TEMPLATE_DIRS = [
    "docs/product",
    "docs/architecture",
    "docs/api",
    "docs/design",
    "docs/security",
    "docs/runbook",
    "docs/reviews",
    "frontend",
    "backend",
    "ai",
    "database/migrations",
    "database/seeds",
    "infra/docker",
    "infra/monitoring",
    "tests/e2e",
    ".github/workflows",
]


def slugify(intent: str) -> str:
    words = re.sub(r"[^a-zA-Z0-9]+", "-", intent.lower()).strip("-")
    return (words[:40] or "project").strip("-")


def ensure_template(root: Path) -> None:
    for rel in TEMPLATE_DIRS:
        d = root / rel
        d.mkdir(parents=True, exist_ok=True)
        keep = d / ".gitkeep"
        if not keep.exists():
            keep.write_text("", encoding="utf-8")
    schema = root / "database" / "schema.sql"
    if not schema.exists():
        schema.write_text("-- current schema snapshot (regenerated after migrations)\n", encoding="utf-8")


def copy_product(projects_root: Path, name: str) -> Path:
    template = projects_root / "_template"
    dest = projects_root / name
    if dest.exists():
        return dest
    ensure_template(template)
    shutil.copytree(template, dest)
    return dest
