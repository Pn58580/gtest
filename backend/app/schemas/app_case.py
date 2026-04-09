from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AppStep(BaseModel):
    action: Literal['launch_app', 'tap', 'input', 'swipe', 'wait', 'assert_text', 'assert_exists']
    target: str = ''
    value: str = ''
    ms: int = 500


class AppCaseItem(BaseModel):
    id: int
    project_id: int
    name: str
    device_id: str
    app_package: str
    app_activity: str
    script_path: str
    steps: list[AppStep] = Field(default_factory=list)
    assert_keyword: str

    model_config = ConfigDict(from_attributes=True)


class AppCaseCreate(BaseModel):
    project_id: int = Field(..., ge=1)
    name: str = Field(..., min_length=2, max_length=128)
    device_id: str = Field(default='emulator-5554')
    app_package: str = Field(default='com.demo.app')
    app_activity: str = Field(default='com.demo.app.MainActivity')
    script_path: str = Field(default='scripts/demo.air')
    steps: list[AppStep] = Field(default_factory=list)
    assert_keyword: str = Field(default='success')


class AppCaseUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=128)
    device_id: str | None = None
    app_package: str | None = None
    app_activity: str | None = None
    script_path: str | None = None
    steps: list[AppStep] | None = None
    assert_keyword: str | None = None
