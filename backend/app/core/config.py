"""
Application settings loaded from environment variables (pydantic-settings).
"""
"""
Application settings, loaded once from environment variables / backend/.env.

- Invalid values stop the app at startup with a clear error.
- Empty values in .env (e.g. "MAX_UPLOAD_MB=") fall back to the defaults below.
- The API key is a SecretStr: it prints as '**********', never the real value.
  It is optional here; the ai module checks it when the provider is created.
"""

from functools import lru_cache
from typing import Annotated, Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_ignore_empty=True, extra="ignore"
    )

    # AI
    ai_provider: Literal["gemini"] = "gemini"
    gemini_api_key: SecretStr = SecretStr("")
    gemini_model: str = ""

    # Upload limits
    max_upload_mb: int = Field(5, gt=0)
    max_image_dimension: int = Field(2048, gt=0)

    # Rate limiting, e.g. "10/minute"
    rate_limit_analyze: str = Field("10/minute", pattern=r"^\d+/(second|minute|hour|day)$")

    # Shared daily cap on ALL AI calls from all visitors (protects the free Gemini quota).
    # 0 = disabled. Set a little below your Gemini free-tier requests/day.
    ai_daily_limit: int = Field(0, ge=0)

    # CORS: comma-separated in .env -> list here
    cors_origins: Annotated[list[str], NoDecode] = ["http://localhost:5173"]

    log_level: LogLevel = "INFO"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: object) -> object:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @field_validator("log_level", mode="before")
    @classmethod
    def _upper_log_level(cls, value: object) -> object:
        return value.upper() if isinstance(value, str) else value

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    """Read settings once and reuse them everywhere."""
    return Settings()