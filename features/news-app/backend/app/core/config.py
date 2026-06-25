"""
Application configuration.
"""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Database
    database_url: str

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 43200  # 30 days

    # OpenAI
    openai_api_key: str | None = None

    # Environment
    environment: str = "development"
    debug: bool = True

    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "capacitor://localhost",
    ]

    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
