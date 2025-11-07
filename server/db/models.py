from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Optional
from uuid import UUID
import uuid

from sqlalchemy import JSON, DateTime, ForeignKey, Numeric, String
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
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
