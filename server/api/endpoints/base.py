"""Базовые пути."""

__author__ = "pv.kosarev"

import json
import logging
from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
    Request,
    Response,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from server.api.schemas.base import ApiInfo
from server.auth.dependencies import get_user_id


templates = Jinja2Templates(directory="server/templates")


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


@base_router.get("/test", response_class=HTMLResponse)
async def root1(request: Request) -> UUID:
    """Корень."""
    return templates.TemplateResponse(
        request=request, name="main.html", context={"data": [
                {"name": "test", "day": "1", "month": "1", "year": "2000"}, 
                {"name": "test1", "day": "10", "month": "1", "year": "2001"},
                {"name": "test2", "day": "31", "month": "1", "year": "2001"},
                {"name": "test2", "day": "31", "month": "1", "year": "2001"},
                {"name": "test2", "day": "31", "month": "2", "year": "2001"},
                {"name": "test2", "day": "5", "month": "3", "year": "2001"},
                {"name": "test2", "day": "20", "month": "12", "year": "2001"},
                {"name": "test2", "day": "15", "month": "11", "year": "2001"},
                {"name": "test2", "day": "12", "month": "1", "year": "2001"},
                ]
            }
        )