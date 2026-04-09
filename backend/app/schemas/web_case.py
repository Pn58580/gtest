from pydantic import BaseModel, ConfigDict, Field


class WebCaseItem(BaseModel):
    id: int
    project_id: int
    name: str
    page_url: str
    selector: str
    expect_text: str

    model_config = ConfigDict(from_attributes=True)


class WebCaseCreate(BaseModel):
    project_id: int = Field(..., ge=1)
    name: str = Field(..., min_length=2, max_length=128)
    page_url: str = Field(default='https://example.com')
    selector: str = Field(default='h1')
    expect_text: str = Field(default='Example')
