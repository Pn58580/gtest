from pydantic import BaseModel, ConfigDict, Field


class ApiCaseItem(BaseModel):
    id: int
    project_id: int
    name: str
    method: str
    path: str
    body: str
    expected_status: int
    expected_keyword: str

    model_config = ConfigDict(from_attributes=True)


class ApiCaseCreate(BaseModel):
    project_id: int = Field(..., ge=1)
    name: str = Field(..., min_length=2, max_length=128)
    method: str = Field(default='GET')
    path: str = Field(default='/')
    body: str = Field(default='{}')
    expected_status: int = Field(default=200, ge=100, le=599)
    expected_keyword: str = Field(default='')
