from __future__ import annotations

from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

AgentName = Literal[
    "jarvis",
    "product",
    "architect",
    "design",
    "frontend",
    "backend",
    "ai_ml",
    "database",
    "code_review",
    "qa",
    "security",
    "devops",
    "documentation",
]

TaskStatus = Literal["pending", "in_progress", "completed", "failed", "blocked"]
ResultStatus = Literal["completed", "failed", "blocked"]


class NeedsFrom(BaseModel):
    agent: str
    artifact: str
    reason: str


class Task(BaseModel):
    task_id: UUID
    intent_id: UUID
    correlation_id: UUID
    issue_key: str | None = None
    agent: str
    status: TaskStatus = "pending"
    depends_on: list[UUID] = Field(default_factory=list)
    input_artifacts: list[str] = Field(default_factory=list)
    output_artifacts: list[str] = Field(default_factory=list)
    model_tier: int = 0
    token_budget: int = 8000
    tokens_used: int = 0
    retry_count: int = 0
    max_retries: int = 3


class AgentResult(BaseModel):
    agent: str
    task_id: UUID
    status: ResultStatus
    summary: str
    artifacts_created: list[str] = Field(default_factory=list)
    artifacts_modified: list[str] = Field(default_factory=list)
    tokens_used: int = 0
    blocking_issues: list[Any] = Field(default_factory=list)
    needs_from: list[NeedsFrom] = Field(default_factory=list)

    @model_validator(mode="after")
    def blocked_requires_needs_from(self) -> AgentResult:
        if self.status == "blocked" and not self.needs_from:
            raise ValueError("blocked results must include needs_from")
        return self
