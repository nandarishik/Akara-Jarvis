from uuid import uuid4

from jarvis.graph import unmet_dependencies
from jarvis.contracts import Task
from jarvis.workers.scopes import assert_in_scope


def test_unmet_dependencies():
    a, b = uuid4(), uuid4()
    task = Task(
        task_id=uuid4(),
        intent_id=uuid4(),
        correlation_id=uuid4(),
        agent="backend",
        depends_on=[a, b],
    )
    assert unmet_dependencies(task, set()) == [a, b]
    assert unmet_dependencies(task, {a}) == [b]
    assert unmet_dependencies(task, {a, b}) == []


def test_backend_scope():
    assert_in_scope("backend/main.py", "backend")
    try:
        assert_in_scope("frontend/page.tsx", "backend")
    except PermissionError:
        return
    raise AssertionError("expected PermissionError")
