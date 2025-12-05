import typer

from fastapi_client_generator import FastapiClientGenerator

cli = typer.Typer(no_args_is_help=True)


@cli.command("from-url")
def generate_from_url(
    client_name: str = typer.Option(
        ..., "--client-name", "-c", help="Name of the generated client package"
    ),
    url: str = typer.Option(..., "--url", "-u", help="URL pointing to the OpenAPI specification"),
):
    """
    Generate a client from a remote OpenAPI URL.
    """
    FastapiClientGenerator(client_name=client_name).from_url(url)
    typer.echo(f"Client '{client_name}' generated from OpenAPI URL: {url}")


@cli.command("from-file")
def generate_from_file(
    client_name: str = typer.Option(
        ..., "--client-name", "-c", help="Name of the generated client package"
    ),
    file_path: str = typer.Option(
        ..., "--file-path", "-f", help="Path to a local OpenAPI JSON/YAML file"
    ),
):
    """
    Generate a client from a local OpenAPI file.
    """
    FastapiClientGenerator(client_name=client_name).from_file_path(file_path)
    typer.echo(f"Client '{client_name}' generated from file: {file_path}")
