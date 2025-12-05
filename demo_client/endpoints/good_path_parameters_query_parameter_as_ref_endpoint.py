from typing import Dict

from ..schemas.item_schema import ItemSchema
from ..utils.request_base import RequestBase


class GoodPathParametersQueryParameterAsRefEndpoint:
    def __init__(self, request_base: RequestBase):
        """This class contains all methods that are available under endpoint `/good-path/parameters/query_parameter_as_ref`."""

        self._request_base = request_base

    def get(self, item_id: ItemSchema, headers: Dict = {}) -> Dict:
        """Calls endpoint `/good-path/parameters/query_parameter_as_ref` as method `get`.

        This checks the handling of a parameter that is a query parameter with a ref.

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.
            - item_id:

        Returns:
            Dict: The response returned by the endpoint.
        """
        response = self._request_base.get(
            uri="/good-path/parameters/query_parameter_as_ref",
            headers={**headers},
            params={**item_id.model_dump()},
        )

        return response.json()
