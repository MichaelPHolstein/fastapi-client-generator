from typing import List, Optional, Union

from fastapi_client_generator.interfaces.builder_interface import BuilderInterface
from fastapi_client_generator.shared.utils import map_oa_ref, map_primitive, pascal_to_snake


class SchemaFieldBuilder(BuilderInterface):
    """
    Generates a single Pydantic field line from an OpenAPI property.
    Handles:
      - primitive types (string, boolean, integer, number)
      - $ref
      - arrays of primitive
      - arrays of $ref
    """

    def __init__(self, field_key: str, field_obj: dict, schema_obj: dict) -> None:
        super().__init__(config=None)
        self._field_key = field_key
        self._field_key_snake_case = pascal_to_snake(field_key)
        self._field_obj = field_obj or {}
        self._schema_obj = schema_obj or {}

    def build(self) -> str:
        """Generates a Pydantic line for the specified field."""
        field_type = self._resolve_type(self._field_obj)

        field_params = [self._determ_default(), *self._determ_common_params(), self._determ_alias()]
        return (
            f"{self._field_key_snake_case}: {self._wrap_optional(field_type)} "
            f"= Field({self._stringify_field_params(field_params)})"
        )

    def _stringify_field_params(self, field_params: List[Optional[str]]) -> str:
        """Converts the Pydantic field parameters into a list of parameters."""
        field_params_filtered = [param for param in field_params if param]
        return ", ".join(field_params_filtered)

    def _wrap_optional(self, resolved_type: str) -> str:
        """Adds Optional[...] if the field is not required."""
        if self._is_required():
            return resolved_type

        return f"Optional[{resolved_type}]"

    def _determ_default(self) -> str:
        """Determines the default for a field."""
        return "default=..." if self._is_required() else "default=None"

    def _determ_common_params(self) -> List[Optional[str]]:
        """
        Check for common OpenAPI fields and map them to Pydantic Field(...)-params.
        Note: keys remain in snake_case (min_length, max_length, description, title).
        """
        common_params = [
            ("description", str),
            ("maxLength", int),
            ("minLength", int),
            ("title", str),
        ]
        return [self._read_optional_field_param(k, t) for k, t in common_params]

    def _determ_alias(self) -> Optional[str]:
        """Adds an alias if the default field name is not in snake_case."""
        if self._field_key_snake_case == self._field_key:
            return None
        return f"alias={repr(self._field_key)}"

    def _read_optional_field_param(self, key: str, _key_type: Union[int, str]) -> Optional[str]:
        """
        Attempts to generate an optional Field(...) argument.
        Converts OpenAPI Pascal/mixCase key to snake_case parameter name.
        Value is safely quoted with repr() if it’s a string.
        """
        if key not in self._field_obj:
            return None

        value = self._field_obj.get(key)
        value_str = repr(value) if isinstance(value, str) else str(value)

        return f"{pascal_to_snake(key)}={value_str}"

    def _is_required(self) -> bool:
        """Determines whether a field is required (based on schema_obj['required'])."""
        required = (self._schema_obj or {}).get("required", []) or []
        return self._field_key in required

    def _resolve_type(self, obj: dict) -> str:
        """
        Determines the Python/Pydantic type as a string.
        Cases:
          - $ref               -> 'RefNameSchema' (or another name, see map_oa_ref)
          - type == 'array'    -> 'List[<resolved item type>]'
          - primitive          -> via mapping
        """
        if "$ref" in obj:
            return map_oa_ref(obj["$ref"])

        field_type = obj.get("type")

        if field_type == "array":
            return self._resolve_array_type(obj)

        return map_primitive(field_type)

    def _resolve_array_type(self, obj: dict) -> str:
        """Processes the field type array."""
        items = obj.get("items", {})

        if not items:
            return "List[Any]"

        item_type = self._resolve_type(items)
        return f"List[{item_type}]"
