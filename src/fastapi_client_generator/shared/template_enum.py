from enum import Enum


class TemplateEnum(str, Enum):
    """Contains all known jinja templates that can be used within the codebase."""

    CLIENT_INIT_TEMPLATE = "client_init_template.jinja"
    CLIENT_BASE_TEMPLATE = "client_base_template.jinja"
    ENDPOINT_TEMPLATE = "endpoint_template.jinja"
    ENDPOINT_METHOD_TEMPLATE = "endpoint_method_template.jinja"
    SCHEMA_BASE_TEMPLATE = "schema_base_template.jinja"
    SCHEMA_OBJECT_TEMPLATE = "schema_object_template.jinja"
    SCHEMA_PRIMITIVE_TEMPLATE = "schema_primitive_template.jinja"
    UTIL_REQUEST_BASE = "util_request_base.jinja"
