from pydantic import BaseModel, ConfigDict, Field


class AppCaseItem(BaseModel):
    id: int
    project_id: int
    name: str
    device_id: str
    app_package: str
    app_activity: str
    script_path: str
    steps_json: str
    assert_keyword: str

    model_config = ConfigDict(from_attributes=True)


class AppCaseCreate(BaseModel):
    project_id: int = Field(..., ge=1)
    name: str = Field(..., min_length=2, max_length=128)
    device_id: str = Field(default='emulator-5554')
    app_package: str = Field(default='com.demo.app')
    app_activity: str = Field(default='com.demo.app.MainActivity')
    script_path: str = Field(default='scripts/demo.air')
    steps_json: str = Field(default='[]')
    assert_keyword: str = Field(default='success')
