from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from datetime import datetime


# Notification Schemas
class NotificationBase(BaseModel):
    day_0: bool = True
    day_1: bool = True
    day_3: bool = False
    day_7: bool = True
    day_14: bool = False
    day_30: bool = False
    day_90: bool = False

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    day_0: Optional[bool] = None
    day_1: Optional[bool] = None
    day_3: Optional[bool] = None
    day_7: Optional[bool] = None
    day_14: Optional[bool] = None
    day_30: Optional[bool] = None
    day_90: Optional[bool] = None

class NotificationRead(NotificationBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True