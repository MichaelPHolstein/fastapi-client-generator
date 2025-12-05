from __future__ import annotations

from pydantic import Field

from .base_schema import BaseSchema


class CartItemSchema(BaseSchema):
    product_id: str = Field(default=...)
    quantity: int = Field(default=...)
