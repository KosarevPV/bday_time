"""Базовые пути."""

__author__ = "pv.kosarev"

import logging
from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
    Response,
)

from server.api.schemas.base import ApiInfo
from server.auth.dependencies import get_user_id

current_logger = logging.getLogger("routes")

base_router = APIRouter()


@base_router.head(
    "/healthcheck",
    description="API health check service route",
    include_in_schema=False,
)
@base_router.get(
    "/healthcheck",
    description="API health check service route",
    include_in_schema=False,
)
def healthcheck() -> Response:
    """Check API health service route."""
    return Response()


@base_router.get("/")
async def root() -> ApiInfo:
    """Корень."""
    return ApiInfo()


@base_router.get("/test")
async def root1(user_id: UUID = Depends(get_user_id)) -> UUID:
    """Корень."""
    return user_id
