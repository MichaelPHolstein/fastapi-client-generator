from typing import Dict

from fastapi_client_generator.interfaces.builder_interface import BuilderInterface
from fastapi_client_generator.shared.utils import map_oa_ref, map_primitive, pascal_to_snake


class EndpointMethodParameterBuilder(BuilderInterface):
    def __init__(
        self,
        method_data: dict,
    ) -> None:
        super().__init__(None)
        self._method_data = method_data

    def build(self) -> Dict:
        """
        Generates the parameters for the endpoint method based on the endpoint data.

        Returns:
            A dict containing parameter information.
        """

        return {
            "functional_arguments": self._create_functional_arguments(),
            "query_parameters": self._create_query_parameters(),
        }

    def _create_functional_arguments(self) -> str:
        """Generates the parameter related functional arguments for the given method.

        Returns:
            A string with all functional arguments
        """
        functional_arguments = [
            self._param_to_func_arg(param) for param in self._method_data.get("parameters", [])
        ]

        arg_with_default = ["headers: Dict = {}"]
        arg_without_default = []

        for functional_argument in functional_arguments:
            if "=" in functional_argument:
                arg_with_default.append(functional_argument)
                continue

            arg_without_default.append(functional_argument)

        return ",".join([*arg_without_default, *arg_with_default])

    def _param_to_func_arg(self, param: dict) -> str:
        """
        Converts the given parameter to a function arg.

        Return:
            Python typed function argument.
        """
        param_name = param.get("name")
        param_name_py = pascal_to_snake(param_name)
        param_type_py = self._determ_param_type(param)

        arg_required = f"{param_name_py}: {param_type_py}"
        arg_optional = f"{param_name_py}: Optional[{param_type_py}] = None"

        return arg_required if param.get("required", False) else arg_optional

    def _determ_param_type(self, param: dict) -> str:
        """
        Generates the param type.

        Returns:
            A primitive python type when found. Returns schema otherwise.
        """
        schema = param.get("schema", {})

        if "$ref" in schema:
            return map_oa_ref(schema.get("$ref"))

        return map_primitive(schema.get("type"))

    def _create_query_parameters(self) -> str:
        """
        Converts OpenAPI query parameters into a valid Python dictionary string
        referencing function arguments.
        """
        query_params = []

        for param in self._method_data.get("parameters", []):
            if param.get("in") != "query":
                continue

            name = param["name"]
            name_py = pascal_to_snake(name)

            schema = param.get("schema", {})
            is_ref = schema.get("$ref", False)

            if is_ref:
                query_params.append(f"**{name_py}.model_dump()")

                continue

            query_params.append(f"'{name}': {name_py}")

        return f"{{{', '.join(query_params)}}}"
