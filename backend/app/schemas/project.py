from pydantic import BaseModel, ConfigDict


class Project(BaseModel):
    id: int
    name: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
