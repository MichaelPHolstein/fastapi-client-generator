from typing import Dict

from ..schemas.item_schema import ItemSchema
from ..utils.request_base import RequestBase


class BadPathMethodNoSummaryEndpoint:
    def __init__(self, request_base: RequestBase):
        """This class contains all methods that are available under endpoint `/bad-path/method/no-summary`."""

        self._request_base = request_base

    def get(self, item_id: str, headers: Dict = {}) -> ItemSchema:
        """Calls endpoint `/bad-path/method/no-summary` as method `get`.

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.
            - item_id (string):

        Returns:
            ItemSchema: The response returned by the endpoint.
        """
        response = self._request_base.get(
            uri="/bad-path/method/no-summary",
            headers={**headers},
            params={},
        )

        return ItemSchema(**response.json())
