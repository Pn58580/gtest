from fastapi import APIRouter

router = APIRouter()


@router.get("/{run_id}")
def get_report(run_id: str) -> dict[str, str]:
    return {"run_id": run_id, "summary": "report is generated"}
