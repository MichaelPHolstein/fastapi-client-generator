from __future__ import annotations

from typing import List

from pydantic import Field

from ..schemas.cart_item_schema import CartItemSchema
from .base_schema import BaseSchema


class OrderSchema(BaseSchema):
    id: str = Field(default=...)
    items: List[CartItemSchema] = Field(default=...)
    total_amount: float = Field(default=...)
    status: str = Field(default=...)
    created_at: str = Field(default=...)
