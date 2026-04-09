from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "L-Tester Pro API"
    database_url: str = "sqlite:///./ltester.db"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    token_expire_minutes: int = 120
    cors_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(env_prefix="LT_", env_file=".env", extra="ignore")

    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(',') if item.strip()]
        return value


settings = Settings()
