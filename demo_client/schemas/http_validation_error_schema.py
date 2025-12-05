from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ..schemas.validation_error_schema import ValidationErrorSchema
from .base_schema import BaseSchema


class HTTPValidationErrorSchema(BaseSchema):
    detail: Optional[List[ValidationErrorSchema]] = Field(default=None, title="Detail")
