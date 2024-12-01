"""Configuration management for Aegis API.

Settings are loaded from environment variables via Pydantic Settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        app_name: Human-readable application name.
        debug: Enable debug mode (more verbose logging, hot-reload, etc.).
        database_url: PostgreSQL connection string.
        secret_key: Secret key used for token signing / encryption.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Aegis API"
    debug: bool = False

    database_url: str = "postgresql+asyncpg://aegis:aegis@localhost:5432/aegis"

    secret_key: str = "change-me-in-production"
