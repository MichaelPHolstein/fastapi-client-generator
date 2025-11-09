from typing import Dict

from fastapi_client_generator.interfaces.builder_interface import BuilderInterface
from fastapi_client_generator.shared.utils import map_oa_ref, map_primitive, pascal_to_snake


class EndpointMethodRequestBodyBuilder(BuilderInterface):
    def __init__(
        self,
        method_data: dict,
    ) -> None:
        super().__init__(None)
        self._method_data = method_data

    def build(self) -> Dict:
        """
        Generates the request body for the endpoint method based on the endpoint data.

        Returns:
            A dict with request body information.
        """

        request_body_exists = self._exists()

        return {
            "exists": self._exists(),
            "functional_arguments": self._create_functional_arguments()
            if request_body_exists
            else "",
        }

    def _exists(self) -> bool:
        """Returns true if method data contains a request body."""
        return "requestBody" in self._method_data

    def _create_functional_arguments(self) -> str:
        """Generates the request_body related functional arguments for the given method."""

        functional_arguments = [self._create_content_type_func_arg()]
        return ",".join(functional_arguments)

    def _create_content_type_func_arg(self) -> str:
        """
        Collects all content types and converts it to functional argument.

        Returns:
            Returns list of available content types.
        """

        request_body: Dict = self._method_data.get("requestBody", {})
        content: Dict = request_body.get("content", {})
        content_types = [content_type for content_type, _ in content.items()]

        content_type_str = ",".join(content_types)

        return f"content_type: Literal['{content_type_str}'] = '{content_types[0]}'"
