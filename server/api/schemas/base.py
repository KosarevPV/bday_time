"""
Базовые схемы Pydantic.
"""

__author__ = "pv.kosarev"

from pydantic import BaseModel, Field

from server.config import settings


class ApiInfo(BaseModel):
    """Информация об API."""

    title: str = Field(description="Имя сервиса", default=settings.API_TITLE)
    description: str = Field(
        description="Описание сервиса", default=settings.API_DESCRIPTION
    )
    version: str = Field(
        description="Текущая версия сервиса", default=settings.API_VERSION
    )
