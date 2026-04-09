from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.models.user import User
from app.schemas.common import RunRequest, RunResult
from app.services.run_service import run_service

router = APIRouter()


@router.post("", response_model=RunResult)
def run_case(
    payload: RunRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> RunResult:
    if not payload.triggered_by:
        payload.triggered_by = current_user.username
    return run_service.execute(db, payload)
