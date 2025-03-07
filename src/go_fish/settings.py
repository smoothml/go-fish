from pathlib import Path

from pydantic import HttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    api_key: str = Field(..., alias="OPENAI_API_KEY")
    base_url: HttpUrl = Field(..., alias="OPENAI_BASE_URL")
    temperature: float = 0.9
    num_agents: int = 3
    log_file: Path | None = None

    model_config = SettingsConfigDict(frozen=True)



def get_settings() -> Settings:
    return Settings()
