from pydantic import BaseModel, ConfigDict


class UserInfo(BaseModel):
    id: int
    username: str
    role: str

    model_config = ConfigDict(from_attributes=True)
