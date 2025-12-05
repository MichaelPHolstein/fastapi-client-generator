from __future__ import annotations

from typing import Any, Optional

from pydantic import Field

from .base_schema import BaseSchema


class AnyOfSchemaSchema(BaseSchema):
    value: Optional[Any] = Field(default=None)
