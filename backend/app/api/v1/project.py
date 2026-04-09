from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.models.user import User
from app.schemas.project import Project, ProjectCreate
from app.services.project_service import project_service

router = APIRouter()


@router.get("/list", response_model=list[Project])
def list_projects(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Project]:
    return project_service.list_projects(db)


@router.post("/create", response_model=Project)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Project:
    return project_service.create_project(db, payload.name, owner_id=current_user.id)
