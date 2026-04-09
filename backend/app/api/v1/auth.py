from fastapi import APIRouter, HTTPException

from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, LoginResponse

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    if payload.username != "admin" or payload.password != "admin123":
        raise HTTPException(status_code=401, detail="invalid credentials")
    return LoginResponse(access_token=create_access_token(payload.username))
