from fastapi import APIRouter

from app.schemas.common import RunRequest, RunResult
from app.services.run_service import run_service

router = APIRouter()


@router.post("", response_model=RunResult)
def run_case(payload: RunRequest) -> RunResult:
    return run_service.execute(payload)
