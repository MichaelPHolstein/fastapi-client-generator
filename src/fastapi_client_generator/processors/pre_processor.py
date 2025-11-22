from fastapi_client_generator.interfaces.processor_interface import ProcessorInterface
from fastapi_client_generator.shared.config import Config


class PreProcessor(ProcessorInterface):
    def __init__(self, config: Config):
        super().__init__(config)

    def run(self):
        """
        Preprocesses the API-client by performing the following steps:

        1. Creating the API-client folder.
        2. Ads the OpenAPI-spec (dict) to the API-client folder.
        """
        self._create_api_client_folder()
        self._create_api_spec_file()

    def _create_api_client_folder(self) -> None:
        """Creates the API-client folder."""
        action = "Creating API-client folder. (ignored when existing)"
        self._config.log_action(action)

        return self._config.file_manager.create_folder(self._config.root_path)

    def _create_api_spec_file(self) -> None:
        """Creates a API-spec file called `api-spec.json` within the API-client folder."""
        self._config.file_manager.save_json(
            file_path=self._config.api_spec_path,
            data=self._config.api_spec,
        )
