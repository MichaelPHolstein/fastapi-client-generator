from typing import List, Tuple

from fastapi_client_generator.builders.endpoints.client_base_builder import ClientBaseBuilder
from fastapi_client_generator.builders.endpoints.endpoint_builder import EndpointBuilder
from fastapi_client_generator.interfaces.processor_interface import ProcessorInterface
from fastapi_client_generator.shared.config import Config
from fastapi_client_generator.shared.utils import pascal_to_snake, snake_to_pascal


class EndpointProcessor(ProcessorInterface):
    def __init__(self, config: Config):
        super().__init__(config)
        self._client_base_classes: List[Tuple[str, str]] = []
        self._client_base_imports: List[str] = []

    def run(self):
        """
        Converts the provided endpoints to functions.

        1. Creates the `/endpoints` folder when non existing.
        2. Generates the endpoints.
        . Generates client base, based on the generated endpoints.

        """
        self._create_endpoint_folder()
        self._create_endpoints()
        self._create_client_base()

    def _create_endpoint_folder(self) -> None:
        """Creates a endpoint folder if it's not existing yet."""
        action = "Creating endpoints folder. (ignored when existing)"
        self._config.log_action(action)

        self._config.file_manager.create_folder(self._config.root_path / "endpoints")

    def _create_endpoints(self) -> None:
        """Collects all paths and converts them to endpoint classes."""

        action = "Generating endpoints"
        self._config.log_action(action)

        for endpoint_path, endpoint_data in self._read_endpoint_data().items():
            endpoint_attribute_name = self._create_endpoint_attribute_name(endpoint_path)
            endpoint_class_name = self._create_endpoint_class_name(endpoint_path)
            endpoint_file_name = self._create_endpoint_file_name(endpoint_path)
            endpoint_import_path = self._create_endpoint_import_path(
                endpoint_file_name, endpoint_class_name
            )

            self._client_base_classes.append((endpoint_attribute_name, endpoint_class_name))
            self._client_base_imports.append(endpoint_import_path)

            EndpointBuilder(
                config=self._config,
                endpoint_class_name=endpoint_class_name,
                endpoint_file_name=endpoint_file_name,
                endpoint_path=endpoint_path,
                endpoint_data=endpoint_data,
            ).build()

    def _create_client_base(self) -> None:
        """Creates the client base of the API-client based on the generated endpoint files."""
        ClientBaseBuilder(
            config=self._config,
            client_base_classes=self._client_base_classes,
            client_base_imports=self._client_base_imports,
        ).build()

    def _create_endpoint_attribute_name(self, endpoint_path: str) -> str:
        """
        Converts endpoints from path into a attribute that is called within the base_client.

        Returns:
            The endpoint path converted to attribute
        """
        return pascal_to_snake(endpoint_path)

    def _create_endpoint_file_name(self, endpoint_path: str) -> str:
        """
        Converts endpoints from path to endpoint_file_name.

        Returns:
            The converted endpoint path
        """
        file_name = pascal_to_snake(endpoint_path)
        return f"{file_name}_endpoint"

    def _create_endpoint_class_name(self, endpoint_path: str) -> str:
        """
        Converts endpoints from path to class names

        Returns:
            The convert endpoint classname
        """
        class_name = snake_to_pascal(endpoint_path)

        return f"{class_name}Endpoint"

    def _create_endpoint_import_path(
        self, endpoint_file_name: str, endpoint_class_name: str
    ) -> str:
        """
        Converts endpoints from path to import path that is used in `client.py`

        Returns:
            The convert endpoint as import path
        """

        return f"from .endpoints.{endpoint_file_name} import {endpoint_class_name}"

    def _read_endpoint_data(self) -> dict:
        """Returns all endpoints paths from the `api-spec.json`."""
        api_spec = self._config.file_manager.load_json(self._config.api_spec_path)
        return api_spec.get("paths", {})
