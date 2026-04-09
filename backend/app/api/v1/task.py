from fastapi import APIRouter, Depends, HTTPException
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


@router.post('/schedule/{schedule_id}/trigger')
def trigger_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, str]:
    ok = task_service.trigger_now(db, schedule_id)
    if not ok:
        raise HTTPException(status_code=404, detail='schedule not found')
    return {'message': 'triggered'}


@router.delete('/schedule/{schedule_id}')
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, str]:
    ok = task_service.delete_schedule(db, schedule_id)
    if not ok:
        raise HTTPException(status_code=404, detail='schedule not found')
    return {'message': 'deleted'}
