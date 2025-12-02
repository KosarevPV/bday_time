

from http import HTTPStatus
from fastapi import Depends, HTTPException, Header
from server.api.schemas.auth import UserRead
from server.services.auth_service import AuthService
from server.services.birthday_service import BirthdayService
from server.services.notification_service import NotificationService
from server.utils.unitofwork import IUnitOfWork, UnitOfWork
from fastapi import status
import logging
from server.config import settings


async def get_birthday_service(
    uow: IUnitOfWork = Depends(UnitOfWork),
) -> BirthdayService:
    return BirthdayService(uow)


async def get_auth_service(
    uow: IUnitOfWork = Depends(UnitOfWork),
) -> AuthService:
    return AuthService(uow)


async def get_notification_service(
    uow: IUnitOfWork = Depends(UnitOfWork),
) -> NotificationService:
    return NotificationService(uow)


async def get_auth_user(user_key: str = Header(), auth_service: AuthService = Depends(get_auth_service)) -> UserRead:
    """Get user_id from X-User-ID header"""
    try:
        return await auth_service.get_user_by_raw_key(raw_key=user_key)
    except ValueError:
        logging.error(f"Invalid user ID format {user_key}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Internal server error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def check_header(microservice_key: str = Header()) -> None:
    if microservice_key != settings.MICROSERVICE_KEY:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Wrong api key.")