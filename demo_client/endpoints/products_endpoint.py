from typing import Dict, Optional

from ..utils.request_base import RequestBase


class ProductsEndpoint:
    def __init__(self, request_base: RequestBase):
        """This class contains all methods that are available under endpoint `/products`."""

        self._request_base = request_base

    def get(
        self,
        headers: Dict = {},
        category: Optional[str] = None,
        search: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ) -> Dict:
        """List all products with filters

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.
            - category (string):
            - search (string):
            - min_price (number):
            - max_price (number):

        Returns:
            Dict: The response returned by the endpoint.
        """
        response = self._request_base.get(
            uri="/products",
            headers={**headers},
            params={
                "category": category,
                "search": search,
                "min_price": min_price,
                "max_price": max_price,
            },
        )

        return response.json()
