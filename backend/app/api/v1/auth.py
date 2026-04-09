from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.user import UserInfo
from app.services.user_service import user_service

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    user = user_service.authenticate(db, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="invalid credentials")
    return LoginResponse(access_token=create_access_token(user.username))


@router.get("/me", response_model=UserInfo)
def me(current_user: User = Depends(get_current_user)) -> UserInfo:
    return UserInfo.model_validate(current_user)
