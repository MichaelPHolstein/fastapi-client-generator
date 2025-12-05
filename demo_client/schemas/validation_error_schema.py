from __future__ import annotations

from typing import Any, List

from pydantic import Field

from .base_schema import BaseSchema


class ValidationErrorSchema(BaseSchema):
    loc: List[Any] = Field(default=..., title="Location")
    msg: str = Field(default=..., title="Message")
    type: str = Field(default=..., title="Error Type")
