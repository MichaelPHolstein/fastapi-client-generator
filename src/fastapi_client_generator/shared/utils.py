import re
from typing import Optional

import requests


def slugify(value: str) -> str:
    """
    Slugifies values.

    Args:
        value: The value to slugify

    Returns:
        The slugified value
    """
    text = value.lower()
    text = re.sub(r"[ .\-/{}]+", "_", text)
    return text.strip("_")


def pascal_to_snake(value: str) -> str:
    """
    Converts Pascal or camel case strings to snake_case and slugifies
    afterwards.

    Returns:
        A snake cased and slugified string
    """
    text = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", value)
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)

    return slugify(text)


def snake_to_pascal(value: str) -> str:
    """
    Converts snake case to pascal case.

    Achieves this by making it snake case first to be sure it will
    properly convert to pascal case.

    Returns:
        A string in pascal case
    """
    parts = slugify(value).strip("_").split("_")
    return "".join(word.capitalize() for word in parts if word)


def map_primitive(primitive_type: Optional[str]) -> str:
    """
    Map OpenAPI primitive to Python type.
    """
    mapping = {
        "string": "str",
        "boolean": "bool",
        "integer": "int",
        "number": "float",
        # fallback:
        None: "Any",
    }
    return mapping.get(primitive_type, "Any")


def convert_ref_to_class_name(ref: str) -> str:
    """
    Converts an OpenAPI schema reference into a schema class name.

    Example:
        '#/components/schemas/ValidationError' -> 'ValidationErrorSchema'
    """
    name = ref.split("/")[-1]
    return f"{name}Schema"


def convert_ref_to_import_path(import_base: str, ref: str) -> str:
    """
    Converts an OpenAPI schema reference into a Python import statement.

    Example:
        '#/components/schemas/ValidationError' ->
        'from client_name.schemas.validation_error_schema import ValidationErrorSchema'
    """
    ref_name = ref.split("/")[-1]
    module = f"{pascal_to_snake(ref_name)}_schema"
    symbol = convert_ref_to_class_name(ref)
    return f"from {import_base}.schemas.{module} import {symbol}"


def download_api_spec_content(api_spec_url: str) -> dict:
    """
    Downloads the API-spec based on the provided `api_spec_url`.

    Raises exception when failed.

    Args:
        api_spec_url: The URL of the OpenAPI spec to download.

    Returns:
        The API-spec content as dict
    """
    response = requests.get(url=api_spec_url, timeout=15)
    response.raise_for_status()
    return response.json()
