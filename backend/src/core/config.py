"""
Core – Configuration
Single source of truth for env vars. Imported by infrastructure only.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = ""
    app_api_key: str = "dev-secret-key"
    default_model: str = "gpt-4o-mini"
    app_version: str = "2.0.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()