from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Sequence
from uuid import UUID

from jarvis.contracts import AgentResult, NeedsFrom, Task
from jarvis.models.router import BudgetExceeded, ModelRouter
from jarvis.workers import gitops
from jarvis.workers.scopes import assert_in_scope

PROMPTS = Path(__file__).resolve().parents[1] / "prompts" / "backend.phase1.md"


def _extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.S)
    if fence:
        text = fence.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < 0:
        raise ValueError("no JSON object in model output")
    return json.loads(text[start : end + 1])


class FallbackWorker:
    def __init__(self, router: ModelRouter, timeout_sec: int) -> None:
        self.router = router
        self.timeout_sec = timeout_sec

    def run(self, task: Task, product_root: Path, scope: Sequence[str]) -> AgentResult:
        gitops.init_develop(product_root)
        slug = "todo-api"
        gitops.create_feature_branch(product_root, task.task_id, slug)
        system = PROMPTS.read_text(encoding="utf-8")
        history: list[dict[str, str]] = [
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": f"Intent task {task.task_id}. Token budget {task.token_budget}. Build the todo API.",
            },
        ]
        tokens = 0
        created: list[str] = []
        modified: list[str] = []
        remaining = task.token_budget
        for _ in range(24):
            try:
                reply, used = self.router.complete(
                    tier=task.model_tier,
                    messages=history,
                    task_id=task.task_id,
                    agent=task.agent,
                    correlation_id=task.correlation_id,
                    budget_remaining=remaining,
                )
            except BudgetExceeded as exc:
                return AgentResult(
                    agent=task.agent,
                    task_id=task.task_id,
                    status="failed",
                    summary=str(exc),
                    tokens_used=tokens,
                )
            tokens += used
            remaining = max(0, task.token_budget - tokens)
            history.append({"role": "assistant", "content": reply})
            try:
                call = _extract_json(reply)
            except (ValueError, json.JSONDecodeError) as exc:
                history.append({"role": "user", "content": f"Invalid JSON ({exc}). Reply with one JSON tool call."})
                continue
            tool = call.get("tool")
            if tool == "done":
                result = call.get("result") or {}
                committed = gitops.commit_all(product_root, result.get("summary") or "feat: backend proof")
                if not committed and not gitops.has_commits_ahead_of_develop(product_root):
                    return AgentResult(
                        agent=task.agent,
                        task_id=task.task_id,
                        status="failed",
                        summary="worker reported success with no git commits",
                        tokens_used=tokens,
                    )
                pr = gitops.open_pr(
                    product_root,
                    task.task_id,
                    title=result.get("summary") or "Phase 1 backend proof",
                    body=result.get("summary") or "",
                )
                arts = list(result.get("artifacts_created") or created)
                if pr.endswith(".md"):
                    arts.append(pr)
                status = result.get("status") or "completed"
                needs = [NeedsFrom(**n) for n in result.get("needs_from") or []]
                return AgentResult(
                    agent=task.agent,
                    task_id=task.task_id,
                    status=status,
                    summary=f"{result.get('summary', '')} PR={pr}",
                    artifacts_created=arts,
                    artifacts_modified=list(result.get("artifacts_modified") or modified),
                    tokens_used=tokens,
                    blocking_issues=list(result.get("blocking_issues") or []),
                    needs_from=needs,
                )
            observation = self._tool(product_root, task.agent, call, created, modified)
            history.append({"role": "user", "content": f"Tool result:\n{observation}"})
        return AgentResult(
            agent=task.agent,
            task_id=task.task_id,
            status="failed",
            summary="max tool iterations exceeded",
            tokens_used=tokens,
        )

    def _tool(
        self,
        root: Path,
        agent: str,
        call: dict[str, Any],
        created: list[str],
        modified: list[str],
    ) -> str:
        tool = call.get("tool")
        if tool == "list_dir":
            path = self._safe(root, agent, call.get("path") or ".", write=False)
            if not path.exists():
                return "missing"
            names = sorted(p.name for p in path.iterdir())
            return "\n".join(names) or "(empty)"
        if tool == "read_file":
            path = self._safe(root, agent, call.get("path") or "", write=False)
            if not path.is_file():
                return "missing file"
            return path.read_text(encoding="utf-8")[:8000]
        if tool == "write_file":
            rel = (call.get("path") or "").replace("\\", "/")
            path = self._safe(root, agent, rel, write=True)
            path.parent.mkdir(parents=True, exist_ok=True)
            existed = path.exists()
            path.write_text(call.get("content") or "", encoding="utf-8")
            if existed:
                modified.append(rel)
            else:
                created.append(rel)
            return f"wrote {rel}"
        if tool == "run_shell":
            command = call.get("command") or ""
            if any(x in command for x in ("..", "rm -rf /", "del /s", "format ")):
                return "rejected"
            proc = subprocess.run(
                command,
                cwd=root,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60,
                env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
            )
            out = (proc.stdout or "") + (proc.stderr or "")
            return out[:4000] or f"exit {proc.returncode}"
        return f"unknown tool {tool}"

    def _safe(self, root: Path, agent: str, rel: str, *, write: bool) -> Path:
        rel = rel.replace("\\", "/").lstrip("/")
        if write:
            assert_in_scope(rel, agent)
        resolved = (root / rel).resolve()
        if not str(resolved).startswith(str(root.resolve())):
            raise PermissionError("path escapes product root")
        return resolved
