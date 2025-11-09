from pathlib import Path
from typing import List

from fastapi_client_generator.builders.endpoints.endpoint_method_builder import (
    EndpointMethodBuilder,
)
from fastapi_client_generator.interfaces.builder_interface import BuilderInterface
from fastapi_client_generator.shared.config import Config
from fastapi_client_generator.shared.template_enum import TemplateEnum


class EndpointBuilder(BuilderInterface):
    def __init__(
        self,
        config: Config,
        endpoint_class_name: str,
        endpoint_file_name: str,
        endpoint_path: str,
        endpoint_data: dict,
    ) -> None:
        super().__init__(config)
        self._endpoint_class_name = endpoint_class_name
        self._endpoint_path = endpoint_path
        self._endpoint_file_name = endpoint_file_name
        self._endpoint_data = endpoint_data

    def build(self):
        """Builds a Python file for given endpoint"""
        self._create_endpoint_file()
        self._create_endpoint_methods()

    def _create_endpoint_file(self) -> None:
        """Creates an Python file for the given endpoint within the endpoint folder."""
        return self._config.file_manager.save_python(
            file_path=self._create_file_path(), code=self._create_code()
        )

    def _create_file_path(self) -> Path:
        """
        Creates a file path for the given endpoint based on the path name.

        Returns:
            The path where the endpoint will be created.
        """
        return self._config.root_path / "endpoints" / f"{self._endpoint_file_name}.py"

    def _create_code(self) -> str:
        """
        Creates the python code for each endpoints that is included within the `endpoint_data`.

        Returns:
            The rendered Jinja template as a string
        """
        return self._config.jinja_env.get_template(
            name=TemplateEnum.ENDPOINT_TEMPLATE.value,
        ).render(
            {
                "endpoint_class_name": self._endpoint_class_name,
                "endpoint_path": self._endpoint_path,
                "endpoint_methods": self._create_endpoint_methods(),
            }
        )

    def _create_endpoint_methods(self) -> List[str]:
        """
        Calls the `EndpointMethodBuilder` for each method available within the given endpoint.
        """

        generated_endpoint_method = []

        for method_name, method_data in self._endpoint_data.items():
            endpoint_method = EndpointMethodBuilder(
                config=self._config,
                endpoint_path=self._endpoint_path,
                method_name=method_name,
                method_data=method_data,
            ).build()

            generated_endpoint_method.append(endpoint_method)

        return generated_endpoint_method
