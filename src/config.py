from functools import lru_cache

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    discord_webhook_url: HttpUrl | None = Field(
        default=None,
        alias="DISCORD_WEBHOOK_URL",
    )
    discord_timeout_seconds: float = Field(
        default=10.0,
        alias="DISCORD_TIMEOUT_SECONDS",
        gt=0,
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
