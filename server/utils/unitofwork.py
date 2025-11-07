from abc import ABC, abstractmethod
from typing import Any

from server.db.database import async_session_maker
from server.repositories.auth_repository import AuthRepository


class IUnitOfWork(ABC):
    auth: AuthRepository

    @abstractmethod
    def __init__(self) -> None: ...

    @abstractmethod
    async def __aenter__(self) -> None: ...

    @abstractmethod
    async def __aexit__(self, *args: Any) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    @abstractmethod
    async def refresh(self, obj: Any) -> None: ...


class UnitOfWork(IUnitOfWork):
    def __init__(self) -> None:
        self.session_factory = async_session_maker

    async def __aenter__(self) -> None:
        self.session = self.session_factory()

        self.auth = AuthRepository(self.session)

    async def __aexit__(self, *args: Any) -> None:
        await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def refresh(self, obj: Any) -> None:
        await self.session.refresh(obj)

    async def rollback(self) -> None:
        await self.session.rollback()
