from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base_schema import BaseSchema


class SelfRefSchemaSchema(BaseSchema):
    self: Optional[SelfRefSchemaSchema] = Field(default=None)
