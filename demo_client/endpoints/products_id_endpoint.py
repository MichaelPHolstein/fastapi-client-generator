from typing import Dict

from ..schemas.product_schema import ProductSchema
from ..utils.request_base import RequestBase


class ProductsIdEndpoint:
    def __init__(self, request_base: RequestBase):
        """This class contains all methods that are available under endpoint `/products/{id}`."""

        self._request_base = request_base

    def get(self, id: str, headers: Dict = {}) -> ProductSchema:
        """Get product details by ID

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.
            - id (string):

        Returns:
            ProductSchema: The response returned by the endpoint.
        """
        response = self._request_base.get(
            uri=f"/products/{id}",
            headers={**headers},
            params={},
        )

        return ProductSchema(**response.json())
