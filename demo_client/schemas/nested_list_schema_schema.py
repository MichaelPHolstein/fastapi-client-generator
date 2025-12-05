from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from .base_schema import BaseSchema


class NestedListSchemaSchema(BaseSchema):
    list: Optional[List[Any]] = Field(default=None)
