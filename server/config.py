"""Файлы конфигураций."""

__author__ = "pv.kosarev"

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="service.env", env_file_encoding="utf-8")

    API_TITLE: str
    API_DESCRIPTION: str
    API_VERSION: str

    MICROSERVICE_KEY: str

    APP_SECRET_KEY: str

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_SCHEMA: str

    DATABASE_URL: str

    DEBUG: bool
    LOG_LEVEL: str = "INFO"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()  # type: ignore
