from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.models.user import User
from app.schemas.app_case import AppCaseCreate, AppCaseItem
from app.schemas.common import RunRequest, RunResult
from app.services.app_case_service import app_case_service
from app.services.environment_service import environment_service
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
    env_id: int | None = Query(default=None, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> RunResult:
    case = app_case_service.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='case not found')

    env = environment_service.get_env(db, env_id) if env_id else environment_service.get_default_env(db, case.project_id)

    request = RunRequest(
        project_id=case.project_id,
        case_id=case.id,
        env_id=env.id if env else None,
        engine='app',
        triggered_by=current_user.username,
        params={
            'device_id': case.device_id,
            'app_package': case.app_package,
            'app_activity': case.app_activity,
            'script_path': case.script_path,
            'steps_json': case.steps_json,
            'assert_keyword': case.assert_keyword,
            'env_name': env.name if env else '',
            'base_url': env.base_url if env else '',
            'env_variables': env.variables_json if env else '{}',
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
