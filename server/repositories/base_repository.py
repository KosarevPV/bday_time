from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Any, Optional

from fastapi import HTTPException
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound


class AbstractRepository(ABC):
    @abstractmethod
    async def get_by_key(self, key: str, value: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> None:
        raise NotImplementedError


class Repository(AbstractRepository):
    model: Any = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_key(self, key: str, value: Any) -> Any:
        try:
            result = await self.session.execute(
                select(self.model).where(getattr(self.model, key) == value)
            )
            return result.scalar_one()
        except NoResultFound:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND.value, detail="Item not found"
            )

    async def get_by_key_multiple(self, key: str, value: Any) -> Any:
        result = await self.session.execute(
            select(self.model).where(getattr(self.model, key) == value)
        )
        return result.scalars().all()

    async def get_all(self, key: Optional[str] = None, value: Any = None) -> Any:
        """Получить все записи."""
        if key is not None and value is not None:
            query = select(self.model).where(getattr(self.model, key) == value)
        else:
            query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_or_create_one(self, data: dict[str, Any]) -> Any:
        try:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await self.session.execute(stmt)
            return res.scalar_one()
        except Exception as e:
            if e.orig.pgcode == "23505":
                await self.session.rollback()
                return await self.get_by_key(key="key", value=data["key"])
            raise


    async def delete_by_key(self, key: str, value: Any) -> None:
        """Удалить по ключу."""
        await self.session.execute(
            delete(self.model).where(getattr(self.model, key) == value)
        )

    async def dellete_all(self) -> None:
        """Удалить все записи."""
        await self.session.execute(delete(self.model))

    async def update_by_key(self, key: str, value: Any, data: dict[str, Any]) -> None:
        """Обновить по ключу."""
        await self.session.execute(
            update(self.model).where(getattr(self.model, key) == value).values(**data)
        ) 
        
