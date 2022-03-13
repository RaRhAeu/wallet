from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr

Str = constr(max_length=255)


class CreateUser(BaseModel):
    email: Str
    password: str
    use_hmac: bool = False


class GetUser(BaseModel):
    email: Str
    use_hmac: bool
    is_superuser: bool
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    password: Optional[str] = None


class User(BaseModel):
    email: Str
    password: str
