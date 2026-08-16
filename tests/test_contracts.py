from pathlib import Path
from uuid import uuid4

import pytest
from pydantic import ValidationError

from jarvis.contracts import AgentResult, NeedsFrom


def test_blocked_requires_needs_from():
    with pytest.raises(ValidationError):
        AgentResult(
            agent="backend",
            task_id=uuid4(),
            status="blocked",
            summary="nope",
        )
    AgentResult(
        agent="backend",
        task_id=uuid4(),
        status="blocked",
        summary="waiting",
        needs_from=[NeedsFrom(agent="architect", artifact="docs/api/contracts.yaml", reason="missing")],
    )
