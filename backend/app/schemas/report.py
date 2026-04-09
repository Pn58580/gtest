from pydantic import BaseModel

from app.schemas.common import StepResult


class ReportResponse(BaseModel):
    run_id: str
    engine: str
    status: str
    duration_ms: int
    triggered_by: str
    steps: list[StepResult]
