"""
Зависимости авторизации.
"""

__author__ = "pv.kosarev"

from http import HTTPStatus
from uuid import UUID

from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.exc import IntegrityError, NoResultFound

from server.api.schemas.auth import UserCreate
from server.services.auth_service import AuthService
from server.utils.unitofwork import IUnitOfWork, UnitOfWork

api_key_header = APIKeyHeader(name="tg-id")


async def get_auth_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> AuthService:
    return AuthService(uow)


async def get_user_id(
    tg_id: str = Security(api_key_header),
    auth_service: AuthService = Depends(get_auth_service),
) -> UUID:
    """
    Получить пользователя.

    :param tg_id: API ключ.
    :return: API ключ.
    """
    try:
        user = await auth_service.create_user(user=UserCreate(key=tg_id))
    except IntegrityError:
        user = await auth_service.get_user_by_raw_key(raw_key=tg_id)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="User not found"
        )
    return user.id
