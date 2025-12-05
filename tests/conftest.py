import shutil
from pathlib import Path

import pytest

from fastapi_client_generator import FastapiClientGenerator

MOCK_CLIENT_NAME = "mock_client"


@pytest.fixture
def local_openapi_spec_path() -> Path:
    """Returns the path of a local mock OpenAPI spec."""
    return Path(__file__).parents[1] / "assets" / "openapi-mock.json"


@pytest.fixture
def fastapi_client_generator() -> FastapiClientGenerator:
    """
    Generates a client generator as fixture so it can be called
    easily from several tests within the test suite.
    """
    return FastapiClientGenerator(
        client_name=MOCK_CLIENT_NAME,
    )


def pytest_unconfigure():
    """Removes the generated client after running tests."""
    mock_client_path = Path(__file__).parents[1] / MOCK_CLIENT_NAME
    shutil.rmtree(mock_client_path)
