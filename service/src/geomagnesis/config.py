from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class _AppConfig(BaseModel):
    ENV: Literal["dev", "prod"]


class _SwaggerUIConfig(BaseModel):
    TITLE: str
    SUMMARY: str
    DESCRIPTION: str
    VERSION: str


class _CorsConfig(BaseModel):
    ALLOW_ORIGINS: list[str]
    ALLOW_METHODS: list[str]
    ALLOW_HEADERS: list[str]
    ALLOW_CREDENTIALS: bool


class _PostgreSQLConfig(BaseModel):
    HOST: str
    PORT: str
    USER: str
    PASSWORD: str
    DB: str
    POOL_SIZE: int
    MAX_OVERFLOW: int
    CONNECTION_TIMEOUT: int
    ECHO: bool
    AUTOFLUSH: bool
    EXPIRE_ON_COMMIT: bool


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__name__).resolve().parent
    STATIC_PATH: Path = (
        BASE_DIR / "src" / "geomagnesis" / "presentations" / "http_api" / "static"
    )
    TEMPLATES_DIR: Path = (
        BASE_DIR / "src" / "geomagnesis" / "presentations" / "http_api" / "templates"
    )

    model_config = SettingsConfigDict(
        env_prefix="GEOMAGNESIS__",
        env_nested_delimiter="__",
        case_sensitive=False,
        env_file=".env",
    )

    app: _AppConfig
    cors: _CorsConfig
    swagger_ui: _SwaggerUIConfig
    postgresql: _PostgreSQLConfig

    @property
    def postgresql_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def swagger_ui_kwargs(self) -> dict[str:str]:
        return {
            "title": self.swagger_ui.TITLE,
            "summary": self.swagger_ui.SUMMARY,
            "description": self.swagger_ui.DESCRIPTION,
            "version": self.swagger_ui.VERSION,
        }


settings = Settings()
