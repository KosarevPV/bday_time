import json
import logging
from uuid import UUID
from async_request import HttpMethod, async_request
from config import settings
from urllib.parse import urljoin

class BackendClient:
    def __init__(self, user_id):
        self.user_id = str(user_id)

    @property
    def headers(self):
        return {
            "user-key": self.user_id,
            "microservice-key": settings.BACKEND_MICROSERVICE_KEY,
        }

    async def create_user(self, user_data: dict):
        response = await async_request(
            method=HttpMethod.POST,
            url=urljoin(settings.BACKEND_URL, "user/"),
            json={
                "key": self.user_id,
                "data": user_data,
            },
            headers=self.headers,
        )

        response.raise_for_status()
        return response

    async def create_birthday(self, name: str, year: int, month: int, day: int):
        response = await async_request(
            method=HttpMethod.POST,
            url=urljoin(settings.BACKEND_URL, "birthdays/"),
            json={
                "name": name,
                "year": year,
                "month": month,
                "day": day,
            },
            headers=self.headers,
        )
        logging.info(response.json())
        response.raise_for_status()
        return response

    async def delete_birthday(self, id: UUID):
        response = await async_request(
            method=HttpMethod.DELETE,
            url=urljoin(settings.BACKEND_URL, f"birthdays/{id}/"),
            headers=self.headers,
        )
        response.raise_for_status()
        return response


    async def get_list_birthdays(self) -> list:
        response = await async_request(
            method=HttpMethod.GET,
            url=urljoin(settings.BACKEND_URL, "birthdays/list"),
            headers=self.headers,
        )
        logging.info(response.json())
        response.raise_for_status()
        return response.json()

    async def get_notification(self) -> dict:
        response = await async_request(
            method=HttpMethod.GET,
            url=urljoin(settings.BACKEND_URL, "notifications/"),
            headers=self.headers,
        )
        logging.info(response.json())
        response.raise_for_status()
        return response.json()

    async def update_notification(
        self,
        day_0: bool,
        day_1: bool,
        day_3: bool,
        day_7: bool,
        day_14: bool,
        day_30: bool,
        day_90: bool
    ) -> None:
        response = await async_request(
            method=HttpMethod.PUT,
            url=urljoin(settings.BACKEND_URL, "notifications/"),
            json={
                "day_0": day_0,
                "day_1": day_1,
                "day_3": day_3,
                "day_7": day_7,
                "day_14": day_14,
                "day_30": day_30,
                "day_90": day_90,
            },
            headers=self.headers,
        )
        logging.info(response.json())
        response.raise_for_status()

        return response.json()