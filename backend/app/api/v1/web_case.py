from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.models.user import User
from app.schemas.common import RunRequest, RunResult
from app.schemas.web_case import WebCaseCreate, WebCaseItem
from app.services.run_service import run_service
from app.services.web_case_service import web_case_service

router = APIRouter()


@router.get('/list', response_model=list[WebCaseItem])
def list_cases(
    project_id: int | None = Query(default=None, ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[WebCaseItem]:
    return web_case_service.list_cases(db, project_id=project_id)


@router.post('/create', response_model=WebCaseItem)
def create_case(
    payload: WebCaseCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> WebCaseItem:
    return web_case_service.create_case(db, payload)


@router.post('/run/{case_id}', response_model=RunResult)
def run_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> RunResult:
    case = web_case_service.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='case not found')

    request = RunRequest(
        project_id=case.project_id,
        case_id=case.id,
        engine='web',
        triggered_by=current_user.username,
        params={
            'page_url': case.page_url,
            'selector': case.selector,
            'expect_text': case.expect_text,
        },
    )
    return run_service.execute(db, request)


@router.delete('/{case_id}')
def delete_case(
    case_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, str]:
    ok = web_case_service.delete_case(db, case_id)
    if not ok:
        raise HTTPException(status_code=404, detail='case not found')
    return {'message': 'deleted'}
