from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CreatePassword(BaseModel):
    login: str
    password: str
    url: Optional[str] = None
    description: Optional[str] = None


class BasePasswordInfo(BaseModel):
    id: UUID
    login: str
    url: Optional[str] = None
    description: Optional[str] = None
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class PasswordInfo(BasePasswordInfo):
    password: str
