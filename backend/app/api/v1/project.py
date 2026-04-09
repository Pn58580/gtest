from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.db import get_db
from app.schemas.project import Project
from app.services.project_service import project_service

router = APIRouter()


@router.get("/list", response_model=list[Project])
def list_projects(db: Session = Depends(get_db)) -> list[Project]:
    return project_service.list_projects(db)
