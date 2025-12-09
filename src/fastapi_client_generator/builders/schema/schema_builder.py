from pathlib import Path
from typing import List, Set, Union

from fastapi_client_generator.builders.schema.schema_field_builder import SchemaFieldBuilder
from fastapi_client_generator.interfaces.builder_interface import BuilderInterface
from fastapi_client_generator.shared.config import Config
from fastapi_client_generator.shared.template_enum import TemplateEnum
from fastapi_client_generator.shared.utils import (
    convert_enum_to_literal,
    convert_ref_to_import_path,
    is_primitive_type,
    map_primitive,
    pascal_to_snake,
)


class SchemaBuilder(BuilderInterface):
    def __init__(
        self,
        config: Config,
        schema_name: str,
        schema_data: dict,
    ) -> None:
        super().__init__(config)
        self._schema_name = schema_name
        self._schema_data = schema_data or {}

    def build(self) -> None:
        """Builds the pydantic schemas for the API-client."""
        self._config.file_manager.save_python(
            file_path=self._create_file_path(),
            code=self._create_code(),
        )

    def _create_file_path(self) -> Path:
        """
        Creates the file_path for the given schema.

        Returns:
            The path of where to create the schema
        """
        file_name = pascal_to_snake(self._schema_name)
        return self._config.root_path / "schemas" / f"{file_name}_schema.py"

    def _create_code(self) -> str:
        """
        Creates the schema code based.

        Returns:
            The rendered Jinja template as string
        """

        schema_type = self._schema_data.get("type")

        if is_primitive_type(schema_type):
            return self._create_primitive_schema()

        return self._create_object_schema()

    def _create_primitive_schema(self) -> str:
        """Converts a OpenAPI primitive type schema to a Pydantic schema."""

        schema_declaration = map_primitive(self._schema_data.get("type"))

        if "enum" in self._schema_data:
            schema_declaration = convert_enum_to_literal(self._schema_data)

        return self._config.jinja_env.get_template(
            name=TemplateEnum.SCHEMA_PRIMITIVE_TEMPLATE.value,
        ).render(
            {
                "schema_name": f"{self._schema_name}Schema",
                "schema_declaration": schema_declaration,
                "description": self._schema_data.get("description"),
            }
        )

    def _create_object_schema(self) -> str:
        """Converts a OpenAPI object type schema to a Pydantic schema."""
        return self._config.jinja_env.get_template(
            name=TemplateEnum.SCHEMA_OBJECT_TEMPLATE.value
        ).render(
            {
                "import_base": self._config.import_base,
                "schema_name": f"{self._schema_name}Schema",
                "schema_fields": self._create_schema_field_list(),
                "import_list": self._create_imports(),
            }
        )

    def _create_schema_field_list(self) -> List[str]:
        """Creates a Pydantic field for each property within the schema using `SchemaFieldBuilder`."""
        properties = self._schema_data.get("properties", {}) or {}
        generated_field_list = []

        for field_key, field_obj in properties.items():
            field_name, field_declaration = SchemaFieldBuilder(
                field_key=field_key, field_obj=field_obj, schema_obj=self._schema_data
            ).build()

            schema_field = f"{field_name}: {field_declaration}"
            generated_field_list.append(schema_field)

        return generated_field_list

    def _create_imports(self) -> List[str]:
        """
        Creates the schema imports where the current schema depends on.

        Returns:
            A list container all required imports.
        """
        ref_list = self._collect_schema_ref_list()
        schema_imports = []

        for ref_name in sorted(ref_list):
            if ref_name == self._schema_name:
                continue

            import_path = convert_ref_to_import_path(
                import_base=self._config.import_base, ref=ref_name
            )
            schema_imports.append(import_path)

        return schema_imports

    def _collect_schema_ref_list(self) -> Set[str]:
        """
        Collects all ref elements from the schema properties object.

        Returns:
            A list of all schemas that are referenced.
        """
        ref_list: Set[str] = set()
        properties: dict = self._schema_data.get("properties", {})

        for prop in properties.values():
            self._walk_node(prop, ref_list)

        return ref_list

    def _walk_node(self, node: Union[dict, list, None], ref_list: Set[str]) -> None:
        """Dispatches to the correct handler based on the node type."""
        if node is None:
            return
        if isinstance(node, dict):
            self._walk_dict(node, ref_list)
        elif isinstance(node, list):
            self._walk_list(node, ref_list)

    def _walk_dict(self, node: dict, ref_list: Set[str]) -> None:
        """Collects all refs from a dict and adds them to the `ref_list`."""

        if "$ref" in node:
            self._add_ref_from_string(node["$ref"], ref_list)

        if node.get("type") == "array":
            self._walk_node(node.get("items"), ref_list)

        for key in ("oneOf", "anyOf", "allOf"):
            if key in node:
                self._walk_node(node[key], ref_list)

        for value in node.values():
            if isinstance(value, (dict, list)):
                self._walk_node(value, ref_list)

    def _walk_list(self, items: list, ref_list: Set[str]) -> None:
        """Walks through a list and triggers `_walk_dict` for each item."""
        for item in items:
            self._walk_node(item, ref_list)

    def _add_ref_from_string(self, ref_str: str, ref_list: Set[str]) -> None:
        """
        Extracts the last section of a $ref string which is the schema name thats is required as import.

        The value is stored within the ref_list.
        """
        parts = ref_str.split("/")
        if parts:
            ref_list.add(parts[-1])
