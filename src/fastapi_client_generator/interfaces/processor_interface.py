from abc import ABC, abstractmethod

from fastapi_client_generator.shared.config import Config


class ProcessorInterface(ABC):
    """Base class for each processor that is used to create the client."""

    def __init__(self, config: Config):
        self._config = config

    @abstractmethod
    def run(self):
        """Executes the processor step."""
