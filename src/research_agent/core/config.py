from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class ApiSettings(BaseModel):
    title: str = "Research Agent API"
    version: str = "0.1.0"
    docs_url: str | None = "/docs"
    redoc_url: str | None = "/redoc"
    openapi_url: str | None = "/openapi.json"


class DatabaseSettings(BaseModel):
    url: PostgresDsn = Field(
        default=PostgresDsn(
            "postgresql+asyncpg://research_agent:research_agent@localhost:5432/research_agent"
        )
    )
    echo: bool = False
    pool_size: int = Field(default=5, ge=1)
    max_overflow: int = Field(default=10, ge=0)


class LoggingSettings(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    format: Literal["plain", "json"] = "plain"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_prefix="RESEARCH_AGENT_",
        extra="ignore",
    )

    app_name: str = "Research Agent"
    environment: Environment = Environment.LOCAL
    debug: bool = False
    api: ApiSettings = Field(default_factory=ApiSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
