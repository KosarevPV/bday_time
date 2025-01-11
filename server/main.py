"""
Точка входа для приложения.
"""

__author__ = "pv.kosarev"

from fastapi import FastAPI

from server.api.endpoints.base import base_router
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

app.include_router(
    base_router,
    prefix="/api/bday_time",
    tags=["base"],
)
