from pydantic import BaseModel, ConfigDict, Field


class Project(BaseModel):
    id: int
    name: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
