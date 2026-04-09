from pydantic import BaseModel, ConfigDict, Field


class AppCaseItem(BaseModel):
    id: int
    project_id: int
    name: str
    device_id: str
    script_path: str
    assert_keyword: str

    model_config = ConfigDict(from_attributes=True)


class AppCaseCreate(BaseModel):
    project_id: int = Field(..., ge=1)
    name: str = Field(..., min_length=2, max_length=128)
    device_id: str = Field(default='emulator-5554')
    script_path: str = Field(default='scripts/demo.air')
    assert_keyword: str = Field(default='success')
