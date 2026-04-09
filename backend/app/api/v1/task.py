from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ScheduleRequest(BaseModel):
    name: str
    cron: str
    engine: str


@router.post("/schedule/create")
def create_schedule(payload: ScheduleRequest) -> dict[str, str]:
    return {
        "message": f"schedule '{payload.name}' created",
        "cron": payload.cron,
        "engine": payload.engine,
    }
