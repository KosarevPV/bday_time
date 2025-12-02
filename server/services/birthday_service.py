from http import HTTPStatus
from typing import Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound

from server.api.schemas.birthday import BirthdayCreate, BirthdayRead
from server.db.models import Birthday
from server.utils.unitofwork import IUnitOfWork
from server.config import settings


class BirthdayService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_birthday(self, id: UUID):
        async with self.uow:
            birthday: Birthday = await self.uow.birthday.get_by_key(key="id", value=id)
            result: BirthdayRead = BirthdayRead.model_validate(birthday)
            return result

    async def get_birthday_list_by_user_id(self, user_id: UUID):
        async with self.uow:
            birthdays: list[Birthday] = await self.uow.birthday.get_by_key_multiple(key="user_id", value=user_id)          
            result: list[BirthdayRead] = [BirthdayRead.model_validate(birthday) for birthday in birthdays]
            return result

    async def create_birthday(self, birthday: BirthdayCreate, user_id: UUID) -> BirthdayRead:
        birthday_dict: dict[str, Any] = birthday.model_dump()
        birthday_dict["user_id"] = user_id
        async with self.uow:
            model: Birthday = await self.uow.birthday.get_or_create_one(birthday_dict)
            result: BirthdayRead = BirthdayRead.model_validate(model)
            await self.uow.commit()

            return result

    async def delete_birthday(self, id: UUID) -> None:
        async with self.uow:
            try:
                await self.uow.birthday.delete_by_key(key="id", value=id)
                await self.uow.commit()
            except NoResultFound:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND.value, detail="Invalid birthday ID"
                )
