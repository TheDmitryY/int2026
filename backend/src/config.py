from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import logging


class Settings(BaseSettings):
    app_name: str = "BetterMeAPI"
    admin_email: str = "test@example.com"
    log_level: str = "INFO"
    PROD_REDIS_ACCOUNT_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()


logging.info(f"Application name {settings.app_name}")
logging.info(f"Application name {settings.admin_email}")
logging.info(f"Application name {settings.log_level}")
