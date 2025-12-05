from typing import Dict, List

from fastapi_client_generator.interfaces.builder_interface import BuilderInterface
from fastapi_client_generator.shared.config import Config
from fastapi_client_generator.shared.utils import (
    convert_ref_to_class_name,
    convert_ref_to_import_path,
)


class EndpointMethodRequestBodyBuilder(BuilderInterface):
    def __init__(
        self,
        config: Config,
        method_data: dict,
    ) -> None:
        super().__init__(config)
        self._method_data = method_data
        self._exists = self._is_existing()
        self._request_body_type = self._determ_request_body_type()  # ← added

    def build(self) -> Dict:
        """
        Generates the request body for the endpoint method based on the endpoint data.

        Returns:
            A dict with request body information.
        """
        return {
            "exists": self._exists,
            "functional_arguments": self._create_functional_arguments(),
            "docstring_args": self._create_docstring_args(),
            "schema_imports": self._create_schema_imports(),
            "request_body_argument": self._create_request_body_argument(),
        }

    def _create_functional_arguments(self) -> str:
        """
        Generates the request_body related functional arguments for the given method.

        Returns:
            A list of request body arguments when requestBody exists in method. Otherwise an empty string.
        """

        if not self._exists:
            return ""

        functional_arguments = [
            self._create_content_type_func_arg(),
            self._create_payload_func_arg(),
        ]
        return ",".join(functional_arguments)

    def _create_docstring_args(self) -> List[str]:
        if not self._exists:
            return []

        return [
            "content_type (string): The content-type that is accepted by the API.",
            f"request_body ({self._request_body_type}): The requested body",  # ← updated
        ]

    def _create_content_type_func_arg(self) -> str:
        """
        Collects all content types and converts it to functional argument.

        Returns:
            Returns list of available content types.
        """

        content = self._read_request_body_content()
        content_types = [content_type for content_type, _ in content.items()]

        content_type_str = ",".join(content_types)

        return f"content_type: Literal['{content_type_str}'] = '{content_types[0]}'"

    def _create_payload_func_arg(self) -> str:
        """
        Creates a functional argument for the request body.

        NOTE: For now the function takes the content of the first content type. Later I will figure out how to make this dynamic.

        Returns:
            A functional argument called request_body that represents the request body.
        """
        content = self._read_request_body_content()

        for _, content_data in content.items():
            return f"request_body: {self._determ_content_data_type(content_data)}"

    def _create_schema_imports(self) -> List[str]:
        """
        Finds all schema references defined in the OpenAPI requestBody and generates Python import statements for them.

        Returns:
            List[str]: A list of fully qualified import paths for the referenced schemas.
        """
        schema_imports = []

        content = self._read_request_body_content()

        for _, content_data in content.items():
            if not self._is_content_reference(content_data):
                continue

            schema: Dict = content_data.get("schema", {})
            schema_import_path = convert_ref_to_import_path(
                import_base=self._config.import_base, ref=schema.get("$ref")
            )
            schema_imports.append(schema_import_path)

        return schema_imports

    def _create_request_body_argument(self) -> str:
        """
        Determines the request_body argument that is sent to the request base.

        Returns:
            The request body argument.
        """
        content = self._read_request_body_content()
        argument = "request_body= request_body"

        for _, content_data in content.items():
            if not self._is_content_reference(content_data):
                return argument

            return f"{argument}.model_dump()"

    def _read_request_body_content(self) -> Dict:
        """
        Reads the content from the request body when existing.

        Returns:
            A dict with all different request body content types. Returns an empty dict when no content.
        """
        request_body: Dict = self._method_data.get("requestBody", {})
        content: Dict = request_body.get("content", {})

        return content

    def _determ_content_data_type(self, content_data: Dict) -> str:
        """
        Determ the content data type.

        Creates the right type based on the content data schema type.

        Returns:
            Returns dict as type when object, otherwise returns the referenced schema.
        """
        if not self._is_content_reference(content_data):
            return "Dict = {}"

        schema: Dict = content_data.get("schema", {})
        schema_class_name = convert_ref_to_class_name(schema.get("$ref"))
        schema_fallback = "{}"
        return f"{schema_class_name} = {schema_fallback}"

    def _determ_request_body_type(self) -> str:
        """
        Determine the Python type for request_body.
        Minimal helper used only for docstrings.
        """
        content = self._read_request_body_content()

        for _, content_data in content.items():
            if self._is_content_reference(content_data):
                schema = content_data.get("schema", {})
                return convert_ref_to_class_name(schema.get("$ref"))
            else:
                return "Dict[str, Any]"

        return "Any"

    def _is_content_reference(self, content_data: Dict) -> bool:
        """Returns True if the content_data is a OpenAPI reference."""
        schema: Dict = content_data.get("schema", {})

        return "$ref" in schema

    def _is_existing(self) -> bool:
        """Returns true if method data contains a request body."""
        return "requestBody" in self._method_data
