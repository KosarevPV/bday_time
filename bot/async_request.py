"""
Общие инструменты.
"""

__author__ = "pv.kosarev"

import logging
from enum import StrEnum
from typing import Any, Dict, Optional

from httpx import AsyncClient, ConnectError, Response
from httpx._types import RequestData, RequestFiles

current_logger = logging.getLogger(__name__)


class HttpMethod(StrEnum):
    """HTTP методы."""

    DELETE = "DELETE"
    GET = "GET"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"


async def async_request(
    method: HttpMethod,
    url: str,
    auth: Optional[tuple[str, str]] = None,
    headers: Optional[Dict[str, Any]] = None,
    data: Optional[RequestData] = None,
    json: Optional[Dict[str, Any]] = None,
    files: Optional[RequestFiles] = None,
    timeout: Optional[int] = 5,
    client_params: Optional[Dict[str, Any]] = None,
) -> Response:
    """
    Асинхронные запросы.

    :param method: HTTP метод (из HttpMethod).
    :param url: Целевой URL.
    :param auth: Базовая аутентификация.
    :param headers: Заголовок.
    :param data: Данные.
    :param json: JSON данные.
    :param files: Файлы.
    :param timeout: Таймаут ожидания ответа.
    :param client_params: Параметры AsyncClient.
    :return: Ответ на запрос.
    """
    async with AsyncClient(**(client_params or {})) as client:
        return await client.request(
            method=str(method.value),
            url=url,
            auth=auth,
            headers=headers,
            data=data,
            json=json,
            files=files,
            timeout=timeout,
        )
