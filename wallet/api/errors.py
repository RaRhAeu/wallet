from typing import Optional

from pydantic import BaseModel, Extra, Field


class ErrorDetails(BaseModel):
    type: Optional[str] = Field(
        None,
        description="Error type",
    )
    title: Optional[str] = Field(None, description="Error title")
    status: int = Field(..., description="Error status")
    detail: str = Field(
        ...,
        description="Error detail",
    )
    instance: Optional[str] = Field(None, description="Error instance")

    def dict(self, **kwargs):
        kwargs.setdefault("exclude_none", True)
        kwargs.setdefault("exclude_unset", True)
        return super().dict(**kwargs)

    class Config:
        extra = Extra.allow


class APIError(Exception):
    def __init__(self, **kwargs):
        self.details = ErrorDetails(**kwargs)


def errors(*statuses: int):
    return {s: {"model": ErrorDetails} for s in statuses} | {
        401: {"model": ErrorDetails}
    }
