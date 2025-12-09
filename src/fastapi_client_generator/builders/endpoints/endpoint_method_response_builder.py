from typing import Dict, List, Optional

from fastapi_client_generator.interfaces.builder_interface import BuilderInterface
from fastapi_client_generator.shared.config import Config
from fastapi_client_generator.shared.utils import (
    convert_ref_to_class_name,
    convert_ref_to_import_path,
)


class EndpointMethodResponseBuilder(BuilderInterface):
    def __init__(
        self,
        config: Config,
        method_data: Dict,
    ) -> None:
        super().__init__(config)

        self._method_data = method_data
        self._content_schema = self._read_content_schema()
        self._response_ref = self._extract_ref(self._content_schema)

    def build(self) -> Dict:
        """
        Generates the response for the endpoint.

        Returns:
            A dict with response information.
        """
        return {
            "response_type": self._create_response_type(),
            "method_response": self._create_method_response(),
            "schema_imports": self._create_schema_imports(),
            "docstring_return": self._create_docstring_return(),
        }

    def _create_response_type(self) -> str:
        """
        Creates the response type for the given endpoint method based on the available responses.

        Returns:
            A schema class name, a list of schemas, or Dict as fallback.
        """
        if self._content_schema:
            schema_type = self._content_schema.get("type")

            # Array of referenced model
            if schema_type == "array":
                items = self._content_schema.get("items", {})
                if "$ref" in items:
                    return f"List[{convert_ref_to_class_name(items['$ref'])}]"

                return "List[Dict]"

            # Single referenced model
            if "$ref" in self._content_schema:
                return convert_ref_to_class_name(self._content_schema["$ref"])

        return "Dict"

    def _create_method_response(self) -> str:
        """
        Creates the response for the method.

        Returns:
            Parsed model instance(s) if a reference exists,
            otherwise the plain JSON response.
        """
        if self._content_schema:
            schema_type = self._content_schema.get("type")

            # Array of referenced model
            if schema_type == "array":
                items = self._content_schema.get("items", {})
                if "$ref" in items:
                    class_name = convert_ref_to_class_name(items["$ref"])
                    return f"[{class_name}(**item) for item in response.json()]"
                return "response.json()"

            # Single referenced model
            if self._response_ref:
                class_name = convert_ref_to_class_name(self._response_ref)
                return f"{class_name}(**response.json())"

        return "response.json()"

    def _create_schema_imports(self) -> List[str]:
        """
        Converts the response ref into import statements.

        Returns:
            List[str]: A list of fully qualified import paths for the referenced schemas.
        """
        if not self._response_ref:
            return []

        import_path = convert_ref_to_import_path(
            import_base=self._config.import_base,
            ref=self._response_ref,
        )
        return [import_path]

    def _create_docstring_return(self) -> str:
        """
        Creates the return annotation for the method docstring.
        """
        response_type = self._create_response_type()
        return f"{response_type}: The response returned by the endpoint."

    def _read_content_schema(self) -> Optional[Dict]:
        """
        Extracts the schema from the first valid 2xx content-type response.

        Returns:
            The schema dict or None.
        """
        responses: Dict = self._method_data.get("responses", {})

        for status, status_info in responses.items():
            if not self._number_in_between(int(status), 200, 299):
                continue

            content = status_info.get("content", {})
            schema = self._read_first_content_type(content)

            if schema:
                return schema

        return None

    def _number_in_between(self, number: int, min: int, max: int) -> bool:
        """
        Determines if the number is between value min and max.

        Returns:
            True if in between.
        """
        return min <= number <= max

    def _read_first_content_type(self, content: Dict) -> Optional[Dict]:
        """
        Returns the schema of the first defined content type.

        Returns:
            The schema dict or None.
        """
        for _, content_data in content.items():
            return content_data.get("schema", {})

        return None

    def _extract_ref(self, schema: Optional[Dict]) -> Optional[str]:
        """
        Finds a $ref in the schema, or in array items.

        Returns:
            The reference string or None.
        """
        if not schema:
            return None

        if "$ref" in schema:
            return schema["$ref"]

        if schema.get("type") == "array":
            items = schema.get("items", {})
            return items.get("$ref")
