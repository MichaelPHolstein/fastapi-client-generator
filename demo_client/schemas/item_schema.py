from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base_schema import BaseSchema


class ItemSchema(BaseSchema):
    id: str = Field(default=..., title="Test")
    name: str = Field(default=...)
    description: Optional[str] = Field(default=None)
