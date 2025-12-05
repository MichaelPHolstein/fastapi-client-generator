from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ..schemas.item_schema import ItemSchema
from .base_schema import BaseSchema


class ItemListResponseSchema(BaseSchema):
    items: Optional[List[ItemSchema]] = Field(default=None)
    total: Optional[int] = Field(default=None)
