from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import require_role
from app.api.deps.db import get_db
from app.models.user import User
from app.schemas.user import UserInfo
from app.services.user_service import user_service

router = APIRouter()


@router.get('/users', response_model=list[UserInfo])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_role('admin')),
) -> list[UserInfo]:
    return [UserInfo.model_validate(item) for item in user_service.list_users(db)]
