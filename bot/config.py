"""Файлы конфигураций."""

__author__ = "pv.kosarev"

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="bot_service.env", env_file_encoding="utf-8")

    BOT_TOKEN: str


settings = Settings()  # type: ignore
