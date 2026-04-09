from pydantic import BaseModel


class RunStats(BaseModel):
    total_runs: int
    passed_runs: int
    failed_runs: int
    api_runs: int
    web_runs: int
    app_runs: int
