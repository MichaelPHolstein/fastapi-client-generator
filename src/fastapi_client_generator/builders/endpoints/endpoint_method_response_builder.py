from typing import Dict, List, Optional

from fastapi_client_generator.interfaces.builder_interface import BuilderInterface
from fastapi_client_generator.shared.utils import (
    convert_ref_to_class_name,
    convert_ref_to_import_path,
)


class EndpointMethodResponseBuilder(BuilderInterface):
    def __init__(
        self,
        method_data: Dict,
    ) -> None:
        super().__init__(None)

        self._method_data = method_data
        self._response_ref = self._read_response_ref()

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
            A schema if the OpenAPI response has a reference. Otherwise it will return a dict.
        """

        if self._response_ref:
            return convert_ref_to_class_name(self._response_ref)

        return "Dict"

    def _create_method_response(self) -> str:
        """
        Creates the response for the method.

        If the endpoint method as a reference, the response will be wrapped around this response.

        Returns:
            Returns the method response
        """

        if self._response_ref:
            response_class_name = convert_ref_to_class_name(self._response_ref)
            return f"{response_class_name}(**response.json())"

        return "response.json()"

    def _create_schema_imports(self) -> List[str]:
        """
        Checks if there is a response ref.

        Converts the ref to import path when found.

        Returns:
            List[str]: A list of fully qualified import paths for the referenced schemas.
        """
        schema_imports = []

        if self._response_ref:
            import_path = convert_ref_to_import_path(self._response_ref)
            schema_imports.append(import_path)

        return schema_imports

    def _create_docstring_return(self) -> str:
        """
        Creates the return argument for the docstring based on the response type.
        """
        if self._response_ref:
            response_type = convert_ref_to_class_name(self._response_ref)
        else:
            response_type = "Dict"

        return f"{response_type}: The response returned by the endpoint."

    def _read_response_ref(self) -> Optional[str]:
        """
        Checks if there is a reference within any of the HTTP 2xx responses of the current endpoint method.

        NOTE: For now only the first content-type is checked.

        Returns:
            The reference when found within the response. Returns nothing otherwise.
        """
        responses: Dict = self._method_data.get("responses", {})

        for status, status_info in responses.items():
            if not self._number_in_between(number=int(status), min=200, max=299):
                continue

            content = status_info.get("content", {})

            return self._read_content_has_ref(content)

    def _number_in_between(self, number: int, min: int, max: int) -> bool:
        """
        Determines if the number is between value min and max.

        Returns:
            True if in between.
        """
        return all(
            [
                number >= min,
                number <= max,
            ]
        )

    def _read_content_has_ref(self, content: Dict) -> Optional[str]:
        """
        This function determines if there is a OpenAPI reference available within the content.

        Returns:
            The first found reference otherwise nothing.
        """
        for _, content_data in content.items():
            schema: Dict = content_data.get("schema", {})

            return schema.get("$ref")
