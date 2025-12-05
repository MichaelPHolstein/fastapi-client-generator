from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base_schema import BaseSchema


class ItemReservedKeywordSchema(BaseSchema):
    from_: Optional[str] = Field(default=None)
