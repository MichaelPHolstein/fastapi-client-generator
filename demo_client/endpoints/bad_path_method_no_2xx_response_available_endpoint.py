from typing import Dict

from ..utils.request_base import RequestBase


class BadPathMethodNo2xxResponseAvailableEndpoint:
    def __init__(self, request_base: RequestBase):
        """This class contains all methods that are available under endpoint `/bad-path/method/no_2xx_response_available`."""

        self._request_base = request_base

    def get(self, item_id: str, headers: Dict = {}) -> Dict:
        """Calls endpoint `/bad-path/method/no_2xx_response_available` as method `get`.

        This specific endpoint does not include a response within the 2xx. Which is normally used to determine the response type.

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.
            - item_id (string):

        Returns:
            Dict: The response returned by the endpoint.
        """
        response = self._request_base.get(
            uri="/bad-path/method/no_2xx_response_available",
            headers={**headers},
            params={},
        )

        return response.json()
