from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.models.user import User
from app.schemas.report import ReportResponse
from app.schemas.stats import RunStats
from app.services.report_service import report_service

router = APIRouter()


@router.get('/stats', response_model=RunStats)
def run_stats(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> RunStats:
    return report_service.get_stats(db)


@router.get('/recent', response_model=list[ReportResponse])
def recent_reports(
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[ReportResponse]:
    return report_service.list_recent(db, limit=limit)


@router.get("/{run_id}", response_model=ReportResponse)
def get_report(
    run_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ReportResponse:
    report = report_service.get_by_run_id(db, run_id)
    if not report:
        raise HTTPException(status_code=404, detail="report not found")
    return report
