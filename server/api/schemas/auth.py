"""
Cхемы ApiKey.
"""

__author__ = "pv.kosarev"

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator

from server.auth.utils import generate_hmac_sha256

from server.config import settings


class UserCreate(BaseModel):
    """Модель для создания объекта user."""

    key: str
    note: str = Field(max_length=64, default="")
    data: dict = Field(default={})

    @field_validator("key")
    @classmethod
    def convert_tg_id_for_key(cls, key: str) -> str:
        return generate_hmac_sha256(key, settings.APP_SECRET_KEY)


class UserRead(BaseModel):
    """Результат создания объекта user."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    key: str = Field(max_length=64)
    note: str = Field(max_length=64)
    data: dict
    created: datetime
