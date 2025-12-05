from typing import Dict

from ..utils.request_base import RequestBase


class CartEndpoint:
    def __init__(self, request_base: RequestBase):
        """This class contains all methods that are available under endpoint `/cart`."""

        self._request_base = request_base

    def get(self, headers: Dict = {}) -> Dict:
        """Get current user's cart

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.

        Returns:
            Dict: The response returned by the endpoint.
        """
        response = self._request_base.get(
            uri="/cart",
            headers={**headers},
            params={},
        )

        return response.json()
