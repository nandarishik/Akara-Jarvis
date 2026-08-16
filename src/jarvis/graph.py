from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from typing import Any, TypedDict
from uuid import UUID, uuid4

from langgraph.graph import END, START, StateGraph

from jarvis.config import Settings
from jarvis.contracts import AgentResult, NeedsFrom, Task
from jarvis.db import store
from jarvis.models.router import ModelRouter
from jarvis.scaffold import copy_product, ensure_template, slugify
from jarvis.workers.fallback import FallbackWorker
from jarvis.workers.openhands import OpenHandsWorker
from jarvis.workers.scopes import SCOPES


class GraphState(TypedDict, total=False):
    intent: str
    intent_id: str
    correlation_id: str
    product_root: str
    task: dict[str, Any]
    result: dict[str, Any]
    error: str


def _task_row(task: Task, result: AgentResult | None = None) -> dict[str, Any]:
    row = {
        "task_id": task.task_id,
        "intent_id": task.intent_id,
        "correlation_id": task.correlation_id,
        "issue_key": task.issue_key,
        "agent": task.agent,
        "status": task.status,
        "depends_on": task.depends_on,
        "input_artifacts": task.input_artifacts,
        "output_artifacts": task.output_artifacts,
        "model_tier": task.model_tier,
        "token_budget": task.token_budget,
        "tokens_used": task.tokens_used,
        "retry_count": task.retry_count,
        "max_retries": task.max_retries,
        "summary": None,
        "blocking_issues": [],
        "needs_from": [],
    }
    if result:
        row["status"] = result.status if result.status != "completed" else "completed"
        row["summary"] = result.summary
        row["tokens_used"] = result.tokens_used
        row["output_artifacts"] = result.artifacts_created + result.artifacts_modified
        row["blocking_issues"] = result.blocking_issues
        row["needs_from"] = [n.model_dump() for n in result.needs_from]
    return row


def unmet_dependencies(task: Task, completed: set[UUID]) -> list[UUID]:
    return [d for d in task.depends_on if d not in completed]


def build_graph(settings: Settings, conn):
    router = ModelRouter(settings, conn)

    def create_intent(state: GraphState) -> GraphState:
        intent_id = uuid4()
        correlation_id = uuid4()
        store.insert_intent(conn, intent_id, correlation_id, state["intent"])
        return {
            **state,
            "intent_id": str(intent_id),
            "correlation_id": str(correlation_id),
        }

    def scaffold_product(state: GraphState) -> GraphState:
        from pathlib import Path

        root = Path(settings.jarvis_projects_root)
        root.mkdir(parents=True, exist_ok=True)
        ensure_template(root / "_template")
        name = slugify(state["intent"])
        dest = copy_product(root, name)
        return {**state, "product_root": str(dest)}

    def plan_tasks(state: GraphState) -> GraphState:
        task = Task(
            task_id=uuid4(),
            intent_id=UUID(state["intent_id"]),
            correlation_id=UUID(state["correlation_id"]),
            agent="backend",
            status="pending",
            model_tier=0,
            token_budget=8000,
            max_retries=3,
        )
        store.upsert_task(conn, _task_row(task))
        return {**state, "task": task.model_dump(mode="json")}

    def run_worker(state: GraphState) -> GraphState:
        from pathlib import Path

        task = Task.model_validate(state["task"])
        blocked = unmet_dependencies(task, set())
        if blocked:
            task.status = "blocked"
            result = AgentResult(
                agent=task.agent,
                task_id=task.task_id,
                status="blocked",
                summary="unmet dependencies",
                needs_from=[
                    NeedsFrom(
                        agent="jarvis",
                        artifact=str(blocked[0]),
                        reason="depends_on not completed",
                    )
                ],
            )
            store.upsert_task(conn, _task_row(task, result))
            return {**state, "result": result.model_dump(mode="json")}

        worker = (
            OpenHandsWorker(settings, conn)
            if settings.worker == "openhands"
            else FallbackWorker(router, settings.task_timeout_sec)
        )
        last: AgentResult | None = None
        while task.retry_count <= task.max_retries:
            task.status = "in_progress"
            store.upsert_task(conn, _task_row(task))
            try:
                with ThreadPoolExecutor(max_workers=1) as pool:
                    fut = pool.submit(
                        worker.run,
                        task,
                        Path(state["product_root"]),
                        SCOPES.get(task.agent, ()),
                    )
                    last = fut.result(timeout=settings.task_timeout_sec)
            except FuturesTimeout:
                task.issue_key = f"{task.task_id}:timeout"
                task.retry_count += 1
                last = AgentResult(
                    agent=task.agent,
                    task_id=task.task_id,
                    status="failed",
                    summary=f"timeout after {settings.task_timeout_sec}s",
                )
            except Exception as exc:  # noqa: BLE001 — surface to task row
                task.issue_key = f"{task.task_id}:worker"
                task.retry_count += 1
                last = AgentResult(
                    agent=task.agent,
                    task_id=task.task_id,
                    status="failed",
                    summary=str(exc),
                )
            else:
                if last.status == "blocked":
                    task.status = "blocked"
                    store.upsert_task(conn, _task_row(task, last))
                    return {**state, "result": last.model_dump(mode="json")}
                if last.status == "completed":
                    task.status = "completed"
                    task.tokens_used = last.tokens_used
                    store.upsert_task(conn, _task_row(task, last))
                    return {**state, "result": last.model_dump(mode="json")}
                task.issue_key = task.issue_key or f"{task.task_id}:worker"
                task.retry_count += 1
            if task.retry_count > task.max_retries:
                break
        assert last is not None
        task.status = "failed"
        store.upsert_task(conn, _task_row(task, last))
        return {**state, "result": last.model_dump(mode="json")}

    g = StateGraph(GraphState)
    g.add_node("create_intent", create_intent)
    g.add_node("scaffold_product", scaffold_product)
    g.add_node("plan_tasks", plan_tasks)
    g.add_node("run_worker", run_worker)
    g.add_edge(START, "create_intent")
    g.add_edge("create_intent", "scaffold_product")
    g.add_edge("scaffold_product", "plan_tasks")
    g.add_edge("plan_tasks", "run_worker")
    g.add_edge("run_worker", END)
    return g


def compile_app(settings: Settings, conn, checkpointer=None):
    builder = build_graph(settings, conn)
    if checkpointer is not None:
        return builder.compile(checkpointer=checkpointer)
    return builder.compile()
