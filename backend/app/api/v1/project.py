from fastapi import APIRouter

from app.schemas.project import Project
from app.services.project_service import project_service

router = APIRouter()


@router.get("/list", response_model=list[Project])
def list_projects() -> list[Project]:
    return project_service.list_projects()
