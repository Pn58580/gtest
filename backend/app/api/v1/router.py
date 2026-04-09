from fastapi import APIRouter

from app.api.v1 import api_case, app_case, auth, environment, project, report, run, system, task, tool_crypto

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(project.router, prefix="/project", tags=["project"])
api_router.include_router(environment.router, prefix='/env', tags=['env'])
api_router.include_router(api_case.router, prefix='/api-case', tags=['api-case'])
api_router.include_router(app_case.router, prefix='/app-case', tags=['app-case'])
api_router.include_router(run.router, prefix="/run", tags=["run"])
api_router.include_router(task.router, prefix="/task", tags=["task"])
api_router.include_router(report.router, prefix="/report", tags=["report"])
api_router.include_router(system.router, prefix="/system", tags=["system"])
api_router.include_router(tool_crypto.router, prefix="/tool/crypto", tags=["tool"])
