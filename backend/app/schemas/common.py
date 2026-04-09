from typing import Any, Literal

from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    project_id: int = Field(..., ge=1)
    case_id: int = Field(..., ge=1)
    engine: Literal["api", "web", "app"]
    triggered_by: str = Field(default="")
    params: dict[str, Any] = Field(default_factory=dict)


class StepResult(BaseModel):
    name: str
    status: Literal["passed", "failed", "skipped"]
    message: str = ""


class RunResult(BaseModel):
    run_id: str
    engine: Literal["api", "web", "app"]
    status: Literal["passed", "failed"]
    duration_ms: int
    steps: list[StepResult] = Field(default_factory=list)
