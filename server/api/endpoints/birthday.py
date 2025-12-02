from fastapi import Response
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from uuid import UUID

from server.api.dependencies import check_header, get_auth_service, get_auth_user, get_birthday_service
from server.api.schemas.birthday import BirthdayRead, BirthdayCreate, BirthdayUpdate
from server.api.schemas.auth import UserRead
from server.services.birthday_service import BirthdayService

birthday_router = APIRouter(prefix="/birthdays", tags=["birthdays"], dependencies=[Depends(check_header)])


@birthday_router.get("/list", response_model=list[BirthdayRead])
async def get_user_birthdays(
    request: Request,
    birthday_service: BirthdayService = Depends(get_birthday_service),
    user: UserRead = Depends(get_auth_user)
):  
    """Get all birthdays for current user"""
    birthdays = await birthday_service.get_birthday_list_by_user_id(user.id)
    return birthdays


@birthday_router.post("/", response_model=BirthdayRead)
async def create_birthday(
    request: Request,
    birthday_in: BirthdayCreate,
    birthday_service: BirthdayService = Depends(get_birthday_service),
    user: UserRead = Depends(get_auth_user)
):
    """Create new birthday"""
    birthday = await birthday_service.create_birthday(birthday_in, user.id)
    return birthday


@birthday_router.delete("/{birthday_id}/")
async def delete_birthday(
    request: Request,
    birthday_id: UUID,
    birthday_service: BirthdayService = Depends(get_birthday_service),
    user: UserRead = Depends(get_auth_user)
):
    """Delete birthday"""
    birthday = await birthday_service.get_birthday(birthday_id)
    if birthday.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this birthday"
        )
    await birthday_service.delete_birthday(birthday_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

