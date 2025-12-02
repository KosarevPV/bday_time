from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Optional
from uuid import UUID
import uuid

from sqlalchemy import JSON, DateTime, ForeignKey, Numeric, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from server.config import settings


class Base(DeclarativeBase):
    """Base."""

    __table_args__ = {"schema": settings.DB_SCHEMA}


class User(Base):
    """User."""

    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    key: Mapped[str] = mapped_column(String(64), unique=True)
    note: Mapped[str] = mapped_column(String(64))
    data: Mapped[JSON] = mapped_column(JSON, default={})
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Birthday(Base):
    """Birthday"""

    __tablename__ = "birthday"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey(f"{settings.DB_SCHEMA}.user.id"))
    name: Mapped[str] = mapped_column(String(64))
    year: Mapped[int] = mapped_column(Numeric(4))
    month: Mapped[int] = mapped_column(Numeric(2))
    day: Mapped[int] = mapped_column(Numeric(2))


class Notification(Base):
    """Notification"""

    __tablename__ = "notification"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey(f"{settings.DB_SCHEMA}.user.id"))
    day_0: Mapped[bool] = mapped_column(Boolean, default=True)
    day_1: Mapped[bool] = mapped_column(Boolean, default=False)
    day_3: Mapped[bool] = mapped_column(Boolean, default=False)
    day_7: Mapped[bool] = mapped_column(Boolean, default=False)
    day_14: Mapped[bool] = mapped_column(Boolean, default=False)
    day_30: Mapped[bool] = mapped_column(Boolean, default=False)
    day_90: Mapped[bool] = mapped_column(Boolean, default=False)
