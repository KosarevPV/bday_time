from fastapi import Response
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from uuid import UUID

from server.api.dependencies import check_header, get_auth_service, get_auth_user, get_notification_service
from server.api.schemas.notification import NotificationRead, NotificationCreate, NotificationUpdate
from server.api.schemas.auth import UserRead
from server.services.notification_service import NotificationService

notification_router = APIRouter(prefix="/notifications", dependencies=[Depends(check_header)])


@notification_router.get("/", response_model=NotificationRead)
async def get_notification(
    request: Request,
    notification_service: NotificationService = Depends(get_notification_service),
    user: UserRead = Depends(get_auth_user)
):  
    """Get all birthdays for current user"""
    notification = await notification_service.get_notification_by_user_id(user.id)
    return notification


@notification_router.put("/", response_model=NotificationRead)
async def update_notification(
    request: Request,
    notification_in: NotificationUpdate,
    notification_service: NotificationService = Depends(get_notification_service),
    user: UserRead = Depends(get_auth_user)
):
    """Update notification"""
    notification = await notification_service.update_notification(notification_in, user.id)
    return notification

