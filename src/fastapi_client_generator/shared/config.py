from pathlib import Path

import typer
from jinja2 import Environment, FileSystemLoader

from fastapi_client_generator.shared.file_manager import FileManager
from fastapi_client_generator.shared.utils import slugify


class Config:
    def __init__(self, api_spec_url: str, client_name: str, client_request_timeout: int = 10):
        # Params
        self.api_spec_url = api_spec_url
        self.client_name = client_name

        # Depends
        self.client_request_timeout = client_request_timeout
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
