from fastapi import APIRouter

from app.api.v1 import auth, project, run, task, report, tool_crypto

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(project.router, prefix="/project", tags=["project"])
api_router.include_router(run.router, prefix="/run", tags=["run"])
api_router.include_router(task.router, prefix="/task", tags=["task"])
api_router.include_router(report.router, prefix="/report", tags=["report"])
api_router.include_router(tool_crypto.router, prefix="/tool/crypto", tags=["tool"])
