from http import HTTPStatus
from typing import Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound

from server.api.schemas.auth import UserCreate, UserRead
from server.auth.utils import generate_hmac_sha256
from server.db.models import User
from server.utils.unitofwork import IUnitOfWork
from server.config import settings


class AuthService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_user_by_raw_key(self, raw_key: str) -> UserRead:
        """
        Получить User ID по "сырому" ключу.
        :param raw_key: Исходный ("сырой") ключ.
        :return: Идентификатор ключа, если он найден в БД.
        """

        async with self.uow:
            user: User = await self.uow.auth.get_by_key(
                key="key", value=generate_hmac_sha256(raw_key, settings.APP_SECRET_KEY)
            )
            result: UserRead = UserRead.model_validate(user)
            return result

    async def create_user(self, user: UserCreate) -> UserRead:
        user_dict: dict[str, Any] = user.model_dump()
        async with self.uow:
            model: User = await self.uow.auth.create_one(user_dict)
            result: UserRead = UserRead.model_validate(model)
            await self.uow.commit()

            return result

    async def delete_user(self, id: UUID) -> None:
        """Удалить api key."""
        async with self.uow:
            try:
                await self.uow.auth.delete_by_key(key="id", value=id)
                await self.uow.commit()
            except NoResultFound:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND.value, detail="Invalid api key ID"
                )
