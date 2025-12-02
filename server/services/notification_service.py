from http import HTTPStatus
from typing import Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound

from server.api.schemas.notification import NotificationCreate, NotificationRead, NotificationUpdate
from server.db.models import Notification
from server.utils.unitofwork import IUnitOfWork
from server.config import settings


class NotificationService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_notification_by_user_id(self, user_id: UUID):
        async with self.uow:
            try:
                notification: Notification = await self.uow.notification.get_by_key(key="user_id", value=user_id)
            except HTTPException:
                notification_dict: dict[str, Any] = NotificationCreate().model_dump()
                notification_dict["user_id"] = user_id  
                notification: Notification = await self.uow.notification.get_or_create_one(notification_dict)
            result: NotificationRead = NotificationRead.model_validate(notification)
            return result

    async def create_notification(self, notification: NotificationCreate, user_id: UUID) -> NotificationRead:
        notification_dict: dict[str, Any] = notification.model_dump()
        notification_dict["user_id"] = user_id
        async with self.uow:
            model: Notification = await self.uow.notification.get_or_create_one(notification_dict)
            result: NotificationRead = NotificationRead.model_validate(model)
            await self.uow.commit()

            return result

    async def update_notification(self, notification: NotificationUpdate, user_id: UUID) -> NotificationRead:
        notification_dict: dict[str, Any] = notification.model_dump()
        notification_dict["user_id"] = user_id
        async with self.uow:
            await self.uow.notification.update_by_key(key="user_id", value=user_id, data=notification_dict)
            model = await self.uow.notification.get_by_key(key="user_id", value=user_id)
            result: NotificationRead = NotificationRead.model_validate(model)
            await self.uow.commit()

            return result
            
    
