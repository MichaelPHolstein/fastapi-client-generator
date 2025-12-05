from typing import Dict, Literal

from ..schemas.order_schema import OrderSchema
from ..utils.request_base import RequestBase


class CheckoutEndpoint:
    def __init__(self, request_base: RequestBase):
        """This class contains all methods that are available under endpoint `/checkout`."""

        self._request_base = request_base

    def post(
        self,
        headers: Dict = {},
        content_type: Literal["application/json"] = "application/json",
        request_body: Dict = {},
    ) -> OrderSchema:
        """Checkout and place order

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.
            - content_type (string): The content-type that is accepted by the API.
            - request_body (Dict[str, Any]): The requested body

        Returns:
            OrderSchema: The response returned by the endpoint.
        """
        response = self._request_base.post(
            uri="/checkout",
            headers={"Content-Type": content_type, **headers},
            params={},
            request_body=request_body,
        )

        return OrderSchema(**response.json())
