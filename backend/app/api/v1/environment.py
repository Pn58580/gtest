from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.models.user import User
from app.schemas.environment import EnvCreate, EnvItem
from app.services.environment_service import environment_service

router = APIRouter()


@router.get('/list', response_model=list[EnvItem])
def list_envs(
    project_id: int | None = Query(default=None, ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[EnvItem]:
    return environment_service.list_envs(db, project_id=project_id)


@router.post('/create', response_model=EnvItem)
def create_env(
    payload: EnvCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> EnvItem:
    return environment_service.create_env(db, payload)


@router.delete('/{env_id}')
def delete_env(
    env_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, str]:
    ok = environment_service.delete_env(db, env_id)
    if not ok:
        raise HTTPException(status_code=404, detail='environment not found')
    return {'message': 'deleted'}
