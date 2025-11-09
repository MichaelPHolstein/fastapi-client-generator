from abc import ABC, abstractmethod

from fastapi_client_generator.shared.config import Config


class BuilderInterface(ABC):
    """Base class for each builder that is used to create the client."""

    def __init__(self, config: Config):
        self._config = config

    @abstractmethod
    def build(self):
        """Builds the specific entity."""
