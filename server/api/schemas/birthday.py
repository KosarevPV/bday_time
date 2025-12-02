from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import List, Optional
from datetime import datetime


# Birthday Schemas
class BirthdayBase(BaseModel):
    name: str
    year: int
    month: int
    day: int

class BirthdayCreate(BirthdayBase):
    pass

class BirthdayUpdate(BaseModel):
    name: Optional[str] = None
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None

class BirthdayRead(BirthdayBase):

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID

