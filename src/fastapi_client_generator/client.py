import json
from pathlib import Path
from typing import Union

from fastapi import FastAPI

from fastapi_client_generator.processors.endpoint_processor import EndpointProcessor
from fastapi_client_generator.processors.post_processor import PostProcessor
from fastapi_client_generator.processors.pre_processor import PreProcessor
from fastapi_client_generator.processors.schema_processor import SchemaProcessor
from fastapi_client_generator.processors.utils_processor import UtilsProcessor
from fastapi_client_generator.shared.config import Config
from fastapi_client_generator.shared.utils import download_api_spec_content


class FastapiClientGenerator:
    def __init__(self, client_name: str):
        """
        FastAPI client generator


        Args:
            client_name: Name of the generated API client.
        """
        self._client_name = client_name

    def from_fastapi(self, fastapi: FastAPI) -> None:
        """
        Generates the API client based on the OpenAPI-spec extracted from a FastAPI instance.

        Args:
            - fastapi: The FastAPI application instance to extract the OpenAPI schema from.
        """
        api_spec = fastapi.openapi()

        config = Config(api_spec=api_spec, client_name=self._client_name)
        return self._generate(config)

    def from_file_path(self, api_spec_file_path: Union[str, Path]) -> None:
        """
        Generates the API client using a local OpenAPI-spec file.

        Args:
            api_spec_file_path: Path to the OpenAPI JSON file.
        """
        path = Path(api_spec_file_path).expanduser().resolve()
        api_spec = json.loads(path.read_text())

        config = Config(api_spec=api_spec, client_name=self._client_name)
        return self._generate(config)

    def from_url(self, api_spec_url: str) -> None:
        """
        Generates the API client using an OpenAPI-spec downloaded from a URL.

        Args:
            api_spec_url: URL pointing to the OpenAPI JSON file.
        """
        api_spec = download_api_spec_content(api_spec_url)

        config = Config(api_spec=api_spec, client_name=self._client_name)
        return self._generate(config)

    def _generate(self, config: Config):
        """
        Runs the generation pipeline for the provided configuration.

        Args:
            config: Configuration object containing the OpenAPI-spec.
        """
        PreProcessor(config).run()
        SchemaProcessor(config).run()
        UtilsProcessor(config).run()
        EndpointProcessor(config).run()
        PostProcessor(config).run()
