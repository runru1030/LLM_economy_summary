import os
from enum import Enum
from functools import cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ENV(Enum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"


@cache
def get_env() -> ENV:
    app_env = os.environ.get("APP_ENV")
    match app_env:
        case "production":
            return ENV.PROD
        case "development":
            return ENV.DEV
        case _:
            return ENV.LOCAL


@cache
def get_env_file() -> Path:
    root_dir = Path(__file__).parent.parent.parent.parent
    return root_dir / f".env.{get_env().value}"


class _DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="db_", env_file=get_env_file(), extra="ignore")

    host: str
    port: int = 5432
    database_name: str = "llm_economy_summary"
    user: str = "dev_user"
    password: str

    def url(self) -> str:
        """Generate async PostgreSQL URL."""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database_name}"

    def sync_url(self) -> str:
        """Generate sync PostgreSQL URL for Alembic."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database_name}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=get_env_file(), extra="ignore")

    db: _DBSettings = Field(default_factory=_DBSettings)  # type: ignore

    @property
    def app_env(self) -> ENV:
        return get_env()

    @property
    def is_local(self) -> bool:
        return self.app_env == ENV.LOCAL

    @property
    def is_dev(self) -> bool:
        return self.app_env == ENV.DEV

    @property
    def is_prod(self) -> bool:
        return self.app_env == ENV.PROD


confisettings = Settings()
