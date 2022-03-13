from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str


class TokenPair(AccessToken):
    refresh_token: str
