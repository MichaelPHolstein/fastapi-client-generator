from typing import List

from fastapi_client_generator.interfaces.builder_interface import BuilderInterface
from fastapi_client_generator.shared.utils import pascal_to_snake


class EndpointMethodDocstringBuilder(BuilderInterface):
    def __init__(
        self,
        method_data: dict,
    ) -> None:
        super().__init__(None)
        self._method_data = method_data

    def build(self) -> str:
        """
        Generates a docstring for the endpoint method based on the endpoint data.

        Returns:
            The generated docstring
        """
        docstring_lines = [self._create_summary(), self._create_description(), *self._create_args()]

        return "\n".join(docstring_lines)

    def _create_summary(self) -> str:
        """
        Creates the docstring summary.

        Checks if available within open-api spec. Generates it based on the method and endpoint path otherwise.

        Returns:
            Summary as docstring line
        """
        if self._method_data.get("summary"):
            return self._method_data.get("summary")

        return f"Calls endpoint `{self._endpoint_path}` as method `{self._method_name}`."

    def _create_description(self) -> str:
        """
        Creates the docstring description if available within method data.
        """
        if self._method_data.get("description"):
            return f"\n{self._method_data.get('description')}\n"

        return ""

    def _create_args(self) -> List[str]:
        """
        Generates arguments for the method docstring.

        Returns:
            A list of arguments. Returns empty list when no params available.
        """
        args_list = ["Args:", self._create_headers_arg()]

        param_list = self._method_data.get("parameters", None)

        if not param_list:
            return args_list

        for param in param_list:
            arg = self._convert_param_to_arg(param)
            args_list.append(arg)

        return args_list

    def _create_headers_arg(self) -> str:
        """Creates a docstring argument for the `headers` param that is always included."""
        return "\t- headers (Dict): HTTP headers that are specifically required for current API endpoint."

    def _convert_param_to_arg(self, param: dict) -> str:
        """Converts an Open-API parameter to a docstring argument."""
        name = pascal_to_snake(param.get("name"))
        param_type = self._read_param_type(param)
        param_description = self._read_param_description(param)

        return f"\t- {name}{param_type}: {param_description}"

    def _read_param_type(self, param: dict) -> str:
        """
        Reads the OpenAPI param type if known.

        Returns:
            Param type if known, empty string otherwise
        """
        schema: dict = param.get("schema", None)

        if not schema:
            return ""

        param_type = schema.get("type", None)

        if not param_type:
            return ""

        return f" ({param_type})"

    def _read_param_description(self, param: dict) -> str:
        """
        Reads the OpenAPI param description if known.

        Returns:
            Description if known, empty string otherwise
        """
        return param.get("description", "")
