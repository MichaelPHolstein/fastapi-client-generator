from fastapi_client_generator.processors.endpoint_processor import EndpointProcessor
from fastapi_client_generator.processors.post_processor import PostProcessor
from fastapi_client_generator.processors.pre_processor import PreProcessor
from fastapi_client_generator.processors.schema_processor import SchemaProcessor
from fastapi_client_generator.processors.utils_processor import UtilsProcessor
from fastapi_client_generator.shared.config import Config


class FastapiClientGenerator:
    def __init__(self, *, api_spec_url: str, client_name: str):
        self._config = Config(api_spec_url=api_spec_url, client_name=client_name)

    def generate(self):
        PreProcessor(self._config).run()
        SchemaProcessor(self._config).run()
        UtilsProcessor(self._config).run()
        EndpointProcessor(self._config).run()
        PostProcessor(self._config).run()
