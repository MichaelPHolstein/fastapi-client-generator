from pathlib import Path
from typing import List, Tuple

from fastapi_client_generator.interfaces.builder_interface import BuilderInterface
from fastapi_client_generator.shared.config import Config
from fastapi_client_generator.shared.template_enum import TemplateEnum


class ClientBaseBuilder(BuilderInterface):
    def __init__(
        self,
        config: Config,
        client_base_classes: List[Tuple[str, str]],
        client_base_imports: List[str],
    ) -> None:
        super().__init__(config)
        self._client_base_classes = client_base_classes
        self._client_base_imports = client_base_imports

    def build(self):
        """
        Build the client base by performing the following actions:

        1. Creates `client.py` which import all endpoints.
        2. Creates `__init__.py` which import the client from `client.py`.

        """

        self._create_client_init()
        self._create_client_base()

    def _create_client_init(self) -> None:
        """Creates a init file that refers to the client in the root folder of the API client."""
        return self._config.file_manager.save_python(
            file_path=self._create_client_init_file_path(), code=self._create_client_init_code()
        )

    def _create_client_base(self) -> None:
        """Creates the client base in the root folder of the project."""
        return self._config.file_manager.save_python(
            file_path=self._create_client_base_file_path(), code=self._create_client_base_code()
        )

    def _create_client_init_file_path(self) -> Path:
        """
        Creates a file path for the `__init__` file.

        Returns:
            The path where the `__init__` will be created
        """
        return self._config.root_path / "__init__.py"

    def _create_client_base_file_path(self) -> Path:
        """
        Creates a file path for the `client.py` file.

        Returns:
            The path where the client will be created
        """
        return self._config.root_path / "client.py"

    def _create_client_init_code(self) -> str:
        """
        Creates the python code for the `__init__` file.

        Returns:
            The rendered Jinja template as a string
        """
        return self._config.jinja_env.get_template(
            name=TemplateEnum.CLIENT_INIT_TEMPLATE.value
        ).render()

    def _create_client_base_code(self) -> str:
        """
        Creates the python code for client base file.

        Returns:
            The rendered Jinja template as a string
        """
        return self._config.jinja_env.get_template(
            name=TemplateEnum.CLIENT_BASE_TEMPLATE.value
        ).render(
            {
                "client_base_classes": self._client_base_classes,
                "client_base_imports": sorted(self._client_base_imports, key=lambda x: x[0]),
                "open_api_spec_url": self._config.api_spec_url,
            }
        )
