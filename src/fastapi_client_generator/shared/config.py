from pathlib import Path
from typing import Dict

import typer
from jinja2 import Environment, FileSystemLoader

from fastapi_client_generator.shared.file_manager import FileManager
from fastapi_client_generator.shared.utils import slugify


class Config:
    def __init__(self, api_spec: Dict, client_name: str):
        """
        Base class that stores imports information.

        This class is initialized in almost every class because it contains the important
        information.

        Args:
            - api_spec (Dict): Contains the OpenAPI specification containing all API-information.
            - client_name (string): The name that the client will have.
        """
        # Params
        self.api_spec = api_spec
        self.client_name = client_name

        # Depends
        self.file_manager = FileManager()
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.templates_path),
        )

    @property
    def api_spec_path(self) -> Path:
        """Determines the path of the API-spec file."""
        return self.root_path / "api-spec.json"

    @property
    def root_path(self) -> Path:
        """
        Determines the root path of the API-client based on the directory where
        the CLI command is executed.

        Returns:
            Root path of the API-client.
        """
        return Path.cwd() / slugify(self.client_name)

    @property
    def import_base(self) -> str:
        """
        The root import namespace used when generating absolute imports
        inside the client package.

        This value determines the top-level package path (e.g. ``my_client``)
        that all generated modules will reference when importing each other.

        Returns:
            The base import path for the generated API client.
        """
        return slugify(self.client_name)

    @property
    def templates_path(self) -> Path:
        """Path to the folder containing all Jinja2 templates."""
        return Path(__file__).resolve().parent.parent / "templates"

    def log_action(self, action: str) -> None:
        """
        Logs the provided action.

        Args:
            action: The action that will be logged.
        """
        typer.echo(f"{action} \n")
