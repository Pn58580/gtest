from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.models.user import User
from app.schemas.task import ScheduleRequest, ScheduleResponse
from app.services.task_service import task_service

router = APIRouter()


@router.post("/schedule/create", response_model=ScheduleResponse)
def create_schedule(
    payload: ScheduleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ScheduleResponse:
    row = task_service.create_schedule(db, payload, creator=current_user.username)
    return ScheduleResponse(
        id=row.id,
        name=row.name,
        cron=row.cron,
        engine=row.engine,
        next_step="job registered to scheduler",
    )


@router.get("/schedule/list")
def list_schedules(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[dict[str, str | int]]:
    rows = task_service.list_schedules(db)
    return [
        {
            "id": row.id,
            "name": row.name,
            "cron": row.cron,
            "engine": row.engine,
            "project_id": row.project_id,
            "case_id": row.case_id,
            "created_by": row.created_by,
        }
        for row in rows
    ]
