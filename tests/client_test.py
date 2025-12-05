from pathlib import Path

from fastapi_client_generator import FastapiClientGenerator
from tests.fastapi_instance import fastapi_instance


def test_generate_client_from_fastapi(fastapi_client_generator: FastapiClientGenerator):
    """Test running the generator using a local OpenAPI spec."""
    assert fastapi_client_generator.from_fastapi(fastapi=fastapi_instance) is None


def test_generate_client_from_file(
    fastapi_client_generator: FastapiClientGenerator, local_openapi_spec_path: Path
):
    """Test running the generator using a local OpenAPI spec."""
    assert (
        fastapi_client_generator.from_file_path(api_spec_file_path=local_openapi_spec_path) is None
    )


def test_generate_client_from_url(
    fastapi_client_generator: FastapiClientGenerator, local_openapi_spec_path: Path
):
    """Test running the generator using an URL."""
    assert (
        fastapi_client_generator.from_url(
            api_spec_url="https://beeceptor.com/docs/storefront-sample.json"
        )
        is None
    )
