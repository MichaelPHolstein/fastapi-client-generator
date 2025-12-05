from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base_schema import BaseSchema


class AddressSchema(BaseSchema):
    line1: str = Field(default=...)
    line2: Optional[str] = Field(default=None)
    city: str = Field(default=...)
    state: str = Field(default=...)
    postal_code: str = Field(default=...)
    country: str = Field(default=...)
