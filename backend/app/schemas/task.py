from pydantic import BaseModel, Field


class ScheduleRequest(BaseModel):
    name: str = Field(..., min_length=2)
    cron: str = Field(..., min_length=9)
    engine: str
    project_id: int = Field(..., ge=1)
    case_id: int = Field(..., ge=1)


class ScheduleResponse(BaseModel):
    id: int
    name: str
    cron: str
    engine: str
    next_step: str
