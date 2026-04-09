from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.api.deps.db import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.services.user_service import user_service

bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    if not credentials:
        raise HTTPException(status_code=401, detail="missing token")

    username = decode_access_token(credentials.credentials)
    if not username:
        raise HTTPException(status_code=401, detail="invalid token")

    user = user_service.get_by_username(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="user not found")

    return user
