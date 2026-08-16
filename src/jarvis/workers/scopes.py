"""Filesystem write scopes. Enforced in the runner, not by asking the model."""

SCOPES: dict[str, tuple[str, ...]] = {
    "product": ("docs/product/",),
    "architect": ("docs/architecture/", "docs/api/"),
    "design": ("docs/design/",),
    "frontend": ("frontend/",),
    "backend": ("backend/",),
    "ai_ml": ("ai/",),
    "database": ("database/",),
    "devops": ("infra/", ".github/"),
    "qa": ("tests/e2e/",),
    "security": ("docs/security/",),
    "documentation": ("docs/runbook/", "README.md", "CHANGELOG.md"),
    "code_review": ("docs/reviews/",),
}


def assert_in_scope(relative_path: str, agent: str) -> None:
    rel = relative_path.replace("\\", "/").lstrip("./")
    allowed = SCOPES.get(agent)
    if allowed is None:
        raise PermissionError(f"unknown agent {agent}")
    if agent == "code_review":
        if not (rel.startswith("docs/reviews/") or rel.startswith("docs/reviews")):
            raise PermissionError("code_review may only write docs/reviews/")
        return
    if agent == "documentation":
        if rel in ("README.md", "CHANGELOG.md") or rel.startswith("docs/runbook/"):
            return
        raise PermissionError("documentation write outside scope")
    if agent == "devops" and (rel.startswith("Dockerfile") or rel.endswith("Dockerfile")):
        return
    for prefix in allowed:
        if rel == prefix.rstrip("/") or rel.startswith(prefix):
            return
    raise PermissionError(f"{agent} cannot write {rel}")
