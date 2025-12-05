from typing import Dict

from ..schemas.order_schema import OrderSchema
from ..utils.request_base import RequestBase


class OrdersOrderidEndpoint:
    def __init__(self, request_base: RequestBase):
        """This class contains all methods that are available under endpoint `/orders/{orderId}`."""

        self._request_base = request_base

    def get(self, order_id: str, headers: Dict = {}) -> OrderSchema:
        """Get order details

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.
            - order_id (string):

        Returns:
            OrderSchema: The response returned by the endpoint.
        """
        response = self._request_base.get(
            uri=f"/orders/{order_id}",
            headers={**headers},
            params={},
        )

        return OrderSchema(**response.json())
