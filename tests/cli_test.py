from pathlib import Path

from typer.testing import CliRunner

from fastapi_client_generator.cli import cli

runner = CliRunner()


def test_generate_from_url():
    """
    Test the CLI command that generates a client from a URL.
    """
    result = runner.invoke(
        cli,
        [
            "from-url",
            "--client-name",
            "demo-client",
            "--url",
            "https://beeceptor.com/docs/storefront-sample.json",
        ],
    )

    assert result.exit_code == 0
    assert (
        "Client 'demo-client' generated from OpenAPI URL: https://beeceptor.com/docs/storefront-sample.json"
        in result.stdout
    )


def test_generate_from_file(local_openapi_spec_path: Path):
    """
    Test the CLI command that generates a client from a local file.
    """
    result = runner.invoke(
        cli,
        [
            "from-file",
            "--client-name",
            "demo-client",
            "--file-path",
            local_openapi_spec_path,
        ],
    )

    assert result.exit_code == 0
    assert f"Client 'demo-client' generated from file: {local_openapi_spec_path}" in result.stdout
