from __future__ import annotations

from pathlib import Path
from typing import Protocol, Sequence

from jarvis.contracts import AgentResult, Task


class Worker(Protocol):
    def run(self, task: Task, product_root: Path, scope: Sequence[str]) -> AgentResult:
        ...
