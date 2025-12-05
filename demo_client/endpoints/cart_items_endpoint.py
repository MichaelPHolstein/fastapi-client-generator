from typing import Dict, Literal

from ..schemas.cart_item_schema import CartItemSchema
from ..utils.request_base import RequestBase


class CartItemsEndpoint:
    def __init__(self, request_base: RequestBase):
        """This class contains all methods that are available under endpoint `/cart/items`."""

        self._request_base = request_base

    def post(
        self,
        headers: Dict = {},
        content_type: Literal["application/json"] = "application/json",
        request_body: CartItemSchema = {},
    ) -> Dict:
        """Add item to cart

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.
            - content_type (string): The content-type that is accepted by the API.
            - request_body (CartItemSchema): The requested body

        Returns:
            Dict: The response returned by the endpoint.
        """
        response = self._request_base.post(
            uri="/cart/items",
            headers={"Content-Type": content_type, **headers},
            params={},
            request_body=request_body.model_dump(),
        )

        return response.json()
