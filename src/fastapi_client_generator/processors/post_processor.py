import subprocess

from fastapi_client_generator.interfaces.processor_interface import ProcessorInterface
from fastapi_client_generator.shared.config import Config


class PostProcessor(ProcessorInterface):
    def __init__(self, config: Config):
        self._config = config

    def run(self):
        """
        Postprocessing the API-client by executing the following steps:

        1. Performs `ruff check [TARGET_PATH] --fix` to fix by Ruff standards.
        2. Performs `ruff format [TARGET_PATH]` to format by Ruff standards.
        3. Removes API-spec from API-client folder.
        """
        self._ruff_check_api_client_folder()
        self._ruff_format_api_client_folder()
        self._remove_api_spec()

    def _ruff_check_api_client_folder(self) -> None:
        """Performs `ruff check --fix` on the API-client folder."""
        action = f"Running 'ruff check' on API-client folder: '{self._config.root_path}'"
        self._config.log_action(action)

        args = ["ruff", "check", self._config.root_path, "--fix"]
        return subprocess.run(args, check=False)

    def _ruff_format_api_client_folder(self) -> None:
        """Performs `ruff format` on the API-client folder."""
        action = f"Running 'ruff format' on API-client folder: '{self._config.root_path}'"
        self._config.log_action(action)

        args = ["ruff", "format", self._config.root_path]
        return subprocess.run(args, check=False)

    def _remove_api_spec(self) -> None:
        """Removes the API-spec file from the client."""
        action = f"Removing API-spec file from API-client folder: '{self._config.api_spec_path}'"
        self._config.log_action(action)

        self._config.file_manager.remove_file(file_path=self._config.api_spec_path)
