from pydantic import BaseModel


class RunHistoryItem(BaseModel):
    run_id: str
    engine: str
    status: str
    duration_ms: int
    triggered_by: str
