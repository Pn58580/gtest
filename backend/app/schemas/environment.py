from pydantic import BaseModel, ConfigDict, Field


class EnvItem(BaseModel):
    id: int
    project_id: int
    name: str
    base_url: str
    variables_json: str

    model_config = ConfigDict(from_attributes=True)


class EnvCreate(BaseModel):
    project_id: int = Field(..., ge=1)
    name: str = Field(..., min_length=2, max_length=64)
    base_url: str = Field(..., min_length=3)
    variables_json: str = Field(default='{}')
