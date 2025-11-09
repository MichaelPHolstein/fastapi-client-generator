import re
from typing import Optional


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


def map_oa_ref(ref: str) -> str:
    """
    Converts OpenAPI schema references to Schemas.

    Example:
        Converts '#/components/schemas/ValidationError' -> 'ValidationErrorSchema'
    """
    name = ref.split("/")[-1]
    return f"{name}Schema"
