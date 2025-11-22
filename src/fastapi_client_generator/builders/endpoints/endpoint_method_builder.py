from typing import Dict

from fastapi_client_generator.builders.endpoints.endpoint_method_docstring_builder import (
    EndpointMethodDocstringBuilder,
)
from fastapi_client_generator.builders.endpoints.endpoint_method_parameter_builder import (
    EndpointMethodParameterBuilder,
)
from fastapi_client_generator.builders.endpoints.endpoint_method_request_body_builder import (
    EndpointMethodRequestBodyBuilder,
)
from fastapi_client_generator.builders.endpoints.endpoint_method_response_builder import (
    EndpointMethodResponseBuilder,
)
from fastapi_client_generator.interfaces.builder_interface import BuilderInterface
from fastapi_client_generator.shared.config import Config
from fastapi_client_generator.shared.template_enum import TemplateEnum
from fastapi_client_generator.shared.utils import pascal_to_snake


class EndpointMethodBuilder(BuilderInterface):
    def __init__(
        self,
        config: Config,
        endpoint_path: str,
        method_name: str,
        method_data: dict,
    ) -> None:
        super().__init__(config)
        self._endpoint_path = endpoint_path
        self._method_name = method_name
        self._method_data = method_data

    def build(self) -> Dict:
        """
        Generates a python function for the given endpoint based on the method information.

        Returns:
            A dictionary containing the method_template and method_imports
        """

        method_docstring = EndpointMethodDocstringBuilder(self._method_data).build()
        method_parameters = EndpointMethodParameterBuilder(self._method_data).build()
        method_request_body = EndpointMethodRequestBodyBuilder(self._method_data).build()
        method_response = EndpointMethodResponseBuilder(self._method_data).build()

        method_function = self._config.jinja_env.get_template(
            name=TemplateEnum.ENDPOINT_METHOD_TEMPLATE.value
        ).render(
            {
                "endpoint_path": self._process_endpoint_path(),
                "method_name": self._method_name,
                "method_docstring": method_docstring,
                "method_parameters": method_parameters,
                "method_request_body": method_request_body,
                "method_response": method_response,
            }
        )

        method_schema_imports = [
            *method_parameters.get("schema_imports", []),
            *method_request_body.get("schema_imports", []),
            *method_response.get("schema_imports", []),
        ]

        return {
            "method_function": method_function,
            "method_schema_imports": method_schema_imports,
        }

    def _process_endpoint_path(self) -> str:
        """
        Processes the endpoint path by replacing path parameters to snake_case variables.

        Returns:
            The endpoint path that is called.
        """
        endpoint_path = self._endpoint_path

        for param in self._method_data.get("parameters", []):
            if param["in"] != "path":
                continue

            endpoint_path = endpoint_path.replace(param["name"], pascal_to_snake(param["name"]))

        return endpoint_path
