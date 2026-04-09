from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "L-Tester Pro API"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    token_expire_minutes: int = 120

    model_config = SettingsConfigDict(env_prefix="LT_", env_file=".env", extra="ignore")


settings = Settings()
