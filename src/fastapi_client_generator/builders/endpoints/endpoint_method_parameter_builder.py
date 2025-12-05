from typing import Dict, List

from fastapi_client_generator.interfaces.builder_interface import BuilderInterface
from fastapi_client_generator.shared.config import Config
from fastapi_client_generator.shared.utils import (
    convert_ref_to_class_name,
    convert_ref_to_import_path,
    map_primitive,
    pascal_to_snake,
)


class EndpointMethodParameterBuilder(BuilderInterface):
    def __init__(
        self,
        config: Config,
        method_data: dict,
    ) -> None:
        super().__init__(config=config)
        self._method_data = method_data

    def build(self) -> Dict:
        """
        Generates the parameters for the endpoint method based on the endpoint data.

        Returns:
            A dict containing parameter information.
        """
        return {
            "functional_arguments": self._create_functional_arguments(),
            "docstring_args": self._create_docstring_args(),
            "query_parameters": self._create_query_parameters(),
            "schema_imports": self._create_schema_imports(),
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

    def _create_docstring_args(self) -> List[str]:
        """
        Generates docstring arguments for parameters.

        Returns:
            A list of arguments. Returns empty list when no params available.
        """

        param_list = self._method_data.get("parameters", None)

        if not param_list:
            return []

        return [self._convert_param_to_arg(param) for param in param_list]

    def _convert_param_to_arg(self, param: Dict) -> str:
        """Converts an Open-API parameter to a docstring argument."""
        name = pascal_to_snake(param.get("name"))
        param_type = self._read_param_type(param)
        param_description = self._read_param_description(param)

        return f"{name}{param_type}: {param_description}"

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

    def _create_schema_imports(self) -> List[str]:
        """Finds all schema references defined in the OpenAPI parameters and generates Python import statements for them.

        Returns:
            List[str]: A list of fully qualified import paths for the referenced schemas.
        """
        schema_imports = []

        for param in self._method_data.get("parameters", []):
            schema = param.get("schema", {})
            is_ref = schema.get("$ref", False)

            if not is_ref:
                continue

            schema_import_path = convert_ref_to_import_path(
                import_base=self._config.import_base, ref=schema.get("$ref")
            )
            schema_imports.append(schema_import_path)

        return schema_imports

    def _determ_param_type(self, param: dict) -> str:
        """
        Generates the param type.

        Returns:
            A primitive python type when found. Returns schema otherwise.
        """
        schema = param.get("schema", {})

        if "$ref" in schema:
            return convert_ref_to_class_name(schema.get("$ref"))

        return map_primitive(schema.get("type"))

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
