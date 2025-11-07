"""
Реализация логирования в проекте.
"""

__author__ = "pv.kosarev"

import logging
import logging.config
import os
from functools import wraps
from typing import Any, Callable

from server.config import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_LOGS_DIR = os.path.join(BASE_DIR, "logs")
BASE_LOG = os.path.join(BASE_DIR, "logs", "root.log")
REQUESTS_LOG = os.path.join(BASE_DIR, "logs", "requests.log")
ALEMBIC_LOG = os.path.join(BASE_DIR, "logs", "alembic.log")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "basic": {
            "format": "%(asctime)s.%(msecs)03d - %(levelname)s - %(name)s : %(message)s",
        },
        "verbose": {
            "format": "[%(asctime)s.%(msecs)03d] - %(levelname)s - %(name)s - %(module)s:%(lineno)d - %(message)s"
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "formatter": "verbose",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_LOG,
            "maxBytes": 2 * 1024 * 1024,  # 2Mb
            "backupCount": 20,  # max log size: 2Mb * 20 = 40
        },
        "requests_file": {
            "level": "INFO",
            "formatter": "verbose",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": REQUESTS_LOG,
            "maxBytes": 2 * 1024 * 1024,  # 2Mb
            "backupCount": 20,  # max log size: 2Mb * 20 = 40
        },
        "stdout": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "verbose",
        },
        "alembic": {
            "level": "INFO",
            "formatter": "verbose",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": ALEMBIC_LOG,
        },
    },
    "loggers": {
        "root": {
            "handlers": ["file", "stdout"],
            "level": "DEBUG" if settings.DEBUG else "WARNING",
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "propagate": False,
            "handlers": ["file", "stdout"],
            "level": "ERROR",
        },
        "requests": {
            "propagate": False,
            "handlers": ["requests_file", "stdout"],
            "level": "INFO",
        },
        "routes": {
            "propagate": False,
            "handlers": ["stdout"],
            "level": "INFO",
        },
    },
}


def setup_logger() -> None:
    """
    Установить конфиг логирования.
    """
    os.makedirs(BASE_LOGS_DIR, exist_ok=True)
    logging.config.dictConfig(LOGGING)


def logged(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Декоратор для логирования входящих и исходящих данных метода.
    """

    @wraps(func)
    def wrapper(*args: tuple[Any, ...], **kwargs: dict[Any, Any]) -> Any:
        """
        Обертка.
        """
        current_logger = logging.getLogger(func.__module__)
        current_logger.info(
            f"START METHOD {func.__name__} with args {args} and " f"kwargs {kwargs}"
        )

        try:
            result = func(*args, **kwargs)
        except Exception:
            current_logger.info(f"END METHOD {func.__name__}")
            raise
        else:
            current_logger.info(f"END METHOD {func.__name__}, result {result}")

        return result

    return wrapper
