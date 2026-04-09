from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.models.user import User
from app.schemas.app_case import AppCaseCreate, AppCaseItem
from app.schemas.common import RunRequest, RunResult
from app.services.app_case_service import app_case_service
from app.services.run_service import run_service

router = APIRouter()


@router.get('/list', response_model=list[AppCaseItem])
def list_cases(
    project_id: int | None = Query(default=None, ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[AppCaseItem]:
    return app_case_service.list_cases(db, project_id=project_id)


@router.post('/create', response_model=AppCaseItem)
def create_case(
    payload: AppCaseCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> AppCaseItem:
    return app_case_service.create_case(db, payload)


@router.post('/run/{case_id}', response_model=RunResult)
def run_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> RunResult:
    case = app_case_service.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='case not found')

    request = RunRequest(
        project_id=case.project_id,
        case_id=case.id,
        engine='app',
        triggered_by=current_user.username,
        params={
            'device_id': case.device_id,
            'script_path': case.script_path,
            'assert_keyword': case.assert_keyword,
        },
    )
    return run_service.execute(db, request)


@router.delete('/{case_id}')
def delete_case(
    case_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, str]:
    ok = app_case_service.delete_case(db, case_id)
    if not ok:
        raise HTTPException(status_code=404, detail='case not found')
    return {'message': 'deleted'}
