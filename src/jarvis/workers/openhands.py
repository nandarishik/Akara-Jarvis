from __future__ import annotations

import platform
import subprocess
from pathlib import Path
from typing import Sequence

from pydantic import SecretStr

from jarvis.config import Settings
from jarvis.contracts import AgentResult, Task
from jarvis.db import store
from jarvis.models.router import ModelRouter
from jarvis.workers import gitops
from jarvis.workers.scopes import assert_in_scope


def docker_daemon_up() -> bool:
    try:
        proc = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        return proc.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def _platform() -> str:
    machine = platform.machine().lower()
    if "arm" in machine or "aarch64" in machine:
        return "linux/arm64"
    return "linux/amd64"


def _out_of_scope_writes(product_root: Path, agent: str) -> list[str]:
    proc = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=product_root,
        capture_output=True,
        text=True,
        check=False,
    )
    bad: list[str] = []
    for line in (proc.stdout or "").splitlines():
        path = line[3:].strip().replace("\\", "/")
        if not path or path.startswith(".git"):
            continue
        try:
            assert_in_scope(path, agent)
        except PermissionError:
            bad.append(path)
    return bad


class OpenHandsWorker:
    """OpenHands Software Agent SDK. Docker when the daemon is up; else local workspace."""

    def __init__(self, settings: Settings, conn) -> None:
        self.settings = settings
        self.conn = conn

    def run(self, task: Task, product_root: Path, scope: Sequence[str]) -> AgentResult:
        try:
            from openhands.sdk import LLM, Conversation
            from openhands.tools.preset.default import get_default_agent
        except ImportError as exc:
            raise RuntimeError(
                "OpenHands SDK is not installed. In the venv run: "
                "pip install openhands-sdk openhands-tools openhands-workspace"
            ) from exc

        gitops.init_develop(product_root)
        gitops.create_feature_branch(product_root, task.task_id, "todo-api")
        product_root = product_root.resolve()

        router = ModelRouter(self.settings, self.conn)
        model_str, api_key = router.openhands_model(task.agent)
        if not api_key:
            raise RuntimeError(
                "No API key for OpenHands model. Set OPENROUTER_API_KEY "
                "(or a primary provider key for this agent)."
            )
        resolved = router.resolve(task.agent)
        llm = LLM(
            usage_id="jarvis-openhands",
            model=model_str,
            api_key=SecretStr(api_key),
        )
        agent = get_default_agent(llm=llm, cli_mode=True)
        prompt = (
            f"You are the {task.agent} agent. Work ONLY under: {', '.join(scope) or 'backend/'}. "
            "Do not write files outside that scope. "
            f"Task: implement the user's request in this product repo at {product_root}. "
            "Create a small FastAPI app under backend/ with GET /healthz and GET /todos. "
            "Commit-quality files; do not delete the rest of the skeleton."
        )

        use_docker = docker_daemon_up()
        mode = "docker" if use_docker else "local"
        if use_docker:
            result = self._run_docker(agent, prompt, product_root)
        else:
            result = self._run_local(agent, prompt, product_root)

        cost = float(result.get("cost") or 0)
        store.log_llm_call(
            self.conn,
            task_id=task.task_id,
            correlation_id=task.correlation_id,
            agent=task.agent,
            model=model_str,
            source=resolved.provider,
            prompt_tokens=0,
            completion_tokens=0,
            usd_estimate=cost,
            would_pause=False,
        )

        bad = _out_of_scope_writes(product_root, task.agent)
        if bad:
            return AgentResult(
                agent=task.agent,
                task_id=task.task_id,
                status="failed",
                summary=f"OpenHands ({mode}) wrote outside scope: {bad}",
            )

        committed = gitops.commit_all(product_root, f"feat: openhands {mode} {task.task_id}")
        if not committed and not gitops.has_commits_ahead_of_develop(product_root):
            return AgentResult(
                agent=task.agent,
                task_id=task.task_id,
                status="failed",
                summary=f"OpenHands ({mode}) produced no git commits (empty workspace?)",
            )
        pr = gitops.open_pr(
            product_root,
            task.task_id,
            title=f"OpenHands {mode} {task.task_id}",
            body=str(result.get("status") or ""),
        )
        return AgentResult(
            agent=task.agent,
            task_id=task.task_id,
            status="completed",
            summary=f"OpenHands {mode}. PR={pr}",
            artifacts_created=[pr] if str(pr).endswith(".md") else [],
            tokens_used=0,
        )

    def _run_local(self, agent, prompt: str, product_root: Path) -> dict:
        from openhands.sdk import Conversation

        conversation = Conversation(agent=agent, workspace=str(product_root))
        try:
            conversation.send_message(prompt)
            conversation.run()
            cost = 0.0
            try:
                cost = float(
                    conversation.conversation_stats.get_combined_metrics().accumulated_cost
                )
            except Exception:
                pass
            status = getattr(conversation.state, "execution_status", "unknown")
            return {"status": str(status), "cost": cost}
        finally:
            conversation.close()

    def _run_docker(self, agent, prompt: str, product_root: Path) -> dict:
        from openhands.sdk import Conversation
        from openhands.workspace import DockerWorkspace

        # Mount is handled by the agent-server image working dir; we copy via prompt
        # and verify host git after. If the mount is empty, no-commit fail applies.
        with DockerWorkspace(
            server_image="ghcr.io/openhands/agent-server:latest-python",
            host_port=18010,
            platform=_platform(),
        ) as workspace:
            probe = workspace.execute_command("pwd && ls")
            if probe.exit_code != 0:
                raise RuntimeError(f"OpenHands Docker workspace unhealthy: {probe.stdout}")
            conversation = Conversation(agent=agent, workspace=workspace)
            try:
                conversation.send_message(
                    prompt
                    + f" Workspace inside the container: {workspace.working_dir}. "
                    "Write files there."
                )
                conversation.run()
                cost = 0.0
                try:
                    cost = float(
                        conversation.conversation_stats.get_combined_metrics().accumulated_cost
                    )
                except Exception:
                    pass
                return {"status": str(conversation.state.execution_status), "cost": cost}
            finally:
                conversation.close()
