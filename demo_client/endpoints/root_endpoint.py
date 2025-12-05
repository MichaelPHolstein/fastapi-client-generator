from typing import Dict

from ..utils.request_base import RequestBase


class RootEndpoint:
    def __init__(self, request_base: RequestBase):
        """This class contains all methods that are available under endpoint `/`."""

        self._request_base = request_base

    def get(self, headers: Dict = {}) -> Dict:
        """Read Root

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.

        Returns:
            Dict: The response returned by the endpoint.
        """
        response = self._request_base.get(
            uri="/",
            headers={**headers},
            params={},
        )

        return response.json()
