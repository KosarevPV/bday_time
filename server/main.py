"""
Точка входа для приложения.
"""

__author__ = "pv.kosarev"

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from server.api.endpoints.base import base_router
from server.api.endpoints.birthday import birthday_router
from server.api.endpoints.user import user_router
from server.api.endpoints.notification import notification_router
from server.config import settings
from server.log import setup_logger

setup_logger()


app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    openapi_url="/api/bday_time/openapi.json",
    docs_url="/api/bday_time/docs",
)

app.mount("/static", StaticFiles(directory="server/static"), name="static")

app.include_router(
    base_router,
    prefix="/api/bday_time",
    tags=["base"],
)

app.include_router(
    birthday_router,
    prefix="/api/bday_time",
    tags=["birthdays"],
)

app.include_router(
    user_router,
    prefix="/api/bday_time",
    tags=["users"],
)

app.include_router(
    notification_router,
    prefix="/api/bday_time",
    tags=["notifications"],
)