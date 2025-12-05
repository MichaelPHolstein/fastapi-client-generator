from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base_schema import BaseSchema


class ItemCreateAliasSchema(BaseSchema):
    pascal_case: Optional[str] = Field(default=None, alias="PascalCase")
