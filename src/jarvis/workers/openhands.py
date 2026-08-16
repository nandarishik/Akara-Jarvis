from __future__ import annotations

from pathlib import Path
from typing import Sequence

from jarvis.contracts import AgentResult, Task


class OpenHandsWorker:
    """Docker OpenHands adapter. Phase 1: not wired until fallback proof is green."""

    def run(self, task: Task, product_root: Path, scope: Sequence[str]) -> AgentResult:
        raise RuntimeError(
            "OpenHands worker is not enabled. Set WORKER=fallback. "
            "See docs/runbook/worker.md."
        )
