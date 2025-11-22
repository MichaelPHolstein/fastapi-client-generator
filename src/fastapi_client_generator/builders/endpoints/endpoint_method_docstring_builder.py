from fastapi_client_generator.interfaces.builder_interface import BuilderInterface


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
        docstring_lines = [self._create_summary(), self._create_description()]

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
