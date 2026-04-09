from typing import Literal

from pydantic import BaseModel, Field


class ScheduleRequest(BaseModel):
    name: str = Field(..., min_length=2)
    cron: str = Field(..., min_length=9)
    engine: Literal['api', 'web', 'app']
    project_id: int = Field(..., ge=1)
    case_id: int = Field(..., ge=1)


class ScheduleResponse(BaseModel):
    id: int
    name: str
    cron: str
    engine: Literal['api', 'web', 'app']
    next_step: str
    job_id: str
