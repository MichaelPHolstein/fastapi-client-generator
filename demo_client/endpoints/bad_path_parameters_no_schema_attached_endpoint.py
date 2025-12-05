from typing import Any, Dict

from ..utils.request_base import RequestBase


class BadPathParametersNoSchemaAttachedEndpoint:
    def __init__(self, request_base: RequestBase):
        """This class contains all methods that are available under endpoint `/bad-path/parameters/no_schema_attached`."""

        self._request_base = request_base

    def get(self, item_id: Any, headers: Dict = {}) -> Dict:
        """Calls endpoint `/bad-path/parameters/no_schema_attached` as method `get`.

        This checks the handling of a parameter without a schema object.

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.
            - item_id:

        Returns:
            Dict: The response returned by the endpoint.
        """
        response = self._request_base.get(
            uri="/bad-path/parameters/no_schema_attached",
            headers={**headers},
            params={},
        )

        return response.json()
