from typing import Dict

from ..schemas.item_schema import ItemSchema
from ..utils.request_base import RequestBase


class ItemsItemIdEndpoint:
    def __init__(self, request_base: RequestBase):
        """This class contains all methods that are available under endpoint `/items/{item_id}`."""

        self._request_base = request_base

    def get(self, item_id: str, headers: Dict = {}) -> ItemSchema:
        """Get item by ID

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.
            - item_id (string):

        Returns:
            ItemSchema: The response returned by the endpoint.
        """
        response = self._request_base.get(
            uri=f"/items/{item_id}",
            headers={**headers},
            params={},
        )

        return ItemSchema(**response.json())
