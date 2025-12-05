from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base_schema import BaseSchema


class ProductSchema(BaseSchema):
    id: str = Field(default=...)
    name: str = Field(default=...)
    description: Optional[str] = Field(default=None)
    price: float = Field(default=...)
    category: str = Field(default=...)
    image_url: Optional[str] = Field(default=None)
    stock: int = Field(default=...)
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)
