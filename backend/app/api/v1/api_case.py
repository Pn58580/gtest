from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.models.user import User
from app.schemas.api_case import ApiCaseCreate, ApiCaseItem
from app.schemas.common import RunRequest, RunResult
from app.services.api_case_service import api_case_service
from app.services.environment_service import environment_service
from app.services.run_service import run_service

router = APIRouter()


@router.get('/list', response_model=list[ApiCaseItem])
def list_cases(
    project_id: int | None = Query(default=None, ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[ApiCaseItem]:
    return api_case_service.list_cases(db, project_id=project_id)


@router.post('/create', response_model=ApiCaseItem)
def create_case(
    payload: ApiCaseCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ApiCaseItem:
    return api_case_service.create_case(db, payload)


@router.post('/run/{case_id}', response_model=RunResult)
def run_case(
    case_id: int,
    env_id: int | None = Query(default=None, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> RunResult:
    case = api_case_service.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='case not found')

    env = environment_service.get_env(db, env_id) if env_id else environment_service.get_default_env(db, case.project_id)

    request = RunRequest(
        project_id=case.project_id,
        case_id=case.id,
        env_id=env.id if env else None,
        engine='api',
        triggered_by=current_user.username,
        params={
            'method': case.method,
            'path': case.path,
            'body': case.body,
            'expected_status': case.expected_status,
            'expected_keyword': case.expected_keyword,
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
    ok = api_case_service.delete_case(db, case_id)
    if not ok:
        raise HTTPException(status_code=404, detail='case not found')
    return {'message': 'deleted'}
