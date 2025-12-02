from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from uuid import UUID

from server.api.dependencies import check_header, get_auth_service, get_auth_user, get_birthday_service, get_notification_service
from server.api.schemas.auth import UserRead, UserCreate
from server.api.schemas.auth import UserRead
from server.api.schemas.notification import NotificationCreate
from server.services.auth_service import AuthService
from server.services.birthday_service import BirthdayService
from server.services.notification_service import NotificationService

user_router = APIRouter(prefix="/user", tags=["users"], dependencies=[Depends(check_header)])


@user_router.get("/list", response_model=list[UserRead])
async def get_users(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Get all users"""
    users = await auth_service.get_all_users()
    return users


@user_router.get("/{user_id}/", response_model=UserRead)
async def get_user(
    user_id: UUID,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Get specific user"""
    user = await auth_service.get_user_by_id(user_id)
    return user


@user_router.post("/", response_model=UserRead)
async def create_user(
    user: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
    notification_service: NotificationService = Depends(get_notification_service),
):
    """Create user"""
    new_user = await auth_service.create_user(user)
    user_notification = await notification_service.create_notification(NotificationCreate(), new_user.id)
    return new_user
