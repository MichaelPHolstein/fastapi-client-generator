from typing import Any, Dict, Optional

from ..utils.request_base import RequestBase


class ItemsItemIdEndpoint:
    def __init__(self, request_base: RequestBase):
        """This class contains all methods that are available under endpoint `/items/{item_id}`."""

        self._request_base = request_base

    def get(self, item_id: int, headers: Dict = {}, q: Optional[Any] = None) -> Dict:
        """Read Item

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.
            - item_id (integer):
            - q:

        Returns:
            Dict: The response returned by the endpoint.
        """
        response = self._request_base.get(
            uri=f"/items/{item_id}",
            headers={**headers},
            params={"q": q},
        )

        return response.json()
