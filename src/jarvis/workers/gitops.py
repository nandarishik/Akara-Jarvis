from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from uuid import UUID


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        text=True,
        capture_output=True,
    )


def init_develop(product_root: Path) -> None:
    git_dir = product_root / ".git"
    if not git_dir.exists():
        _git(product_root, "init", "-b", "develop")
        _git(product_root, "config", "user.email", "jarvis@local")
        _git(product_root, "config", "user.name", "JARVIS")
        _git(product_root, "add", "-A")
        _git(product_root, "commit", "-m", "chore: product skeleton")


def create_feature_branch(product_root: Path, task_id: UUID, slug: str) -> str:
    short = str(task_id).split("-")[0]
    branch = f"feature/TASK-{short}-{slug}"[:80]
    _git(product_root, "checkout", "develop")
    _git(product_root, "checkout", "-B", branch)
    return branch


def commit_all(product_root: Path, message: str) -> bool:
    _git(product_root, "add", "-A")
    staged = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=product_root,
    )
    if staged.returncode == 0:
        return False
    _git(product_root, "commit", "-m", message)
    return True


def has_commits_ahead_of_develop(product_root: Path) -> bool:
    proc = subprocess.run(
        ["git", "rev-list", "--count", "develop..HEAD"],
        cwd=product_root,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        return False
    return int((proc.stdout or "0").strip() or "0") > 0


def open_pr(product_root: Path, task_id: UUID, title: str, body: str) -> str:
    origin = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=product_root,
        capture_output=True,
        text=True,
    )
    gh = shutil.which("gh")
    if origin.returncode == 0 and gh:
        subprocess.run(
            ["gh", "pr", "create", "--base", "develop", "--title", title, "--body", body],
            cwd=product_root,
            check=False,
        )
        return "github-pr"
    reviews = product_root / "docs" / "reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    path = reviews / f"LOCAL_PR-{task_id}.md"
    path.write_text(f"# {title}\n\nBase: `develop`\n\n{body}\n", encoding="utf-8")
    commit_all(product_root, f"docs: local PR for {task_id}")
    return str(path.relative_to(product_root)).replace("\\", "/")
