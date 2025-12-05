from typing import Dict

from ..schemas.item_schema import ItemSchema
from ..utils.request_base import RequestBase


class EndpointWithDescriptionEndpoint:
    def __init__(self, request_base: RequestBase):
        """This class contains all methods that are available under endpoint `/endpoint/with-description`."""

        self._request_base = request_base

    def get(self, item_id: str, headers: Dict = {}) -> ItemSchema:
        """This endpoint includes a description

        This is an endpoint with a description included.

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.
            - item_id (string):

        Returns:
            ItemSchema: The response returned by the endpoint.
        """
        response = self._request_base.get(
            uri="/endpoint/with-description",
            headers={**headers},
            params={},
        )

        return ItemSchema(**response.json())
