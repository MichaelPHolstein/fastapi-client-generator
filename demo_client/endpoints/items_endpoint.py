from typing import Dict, Literal

from ..schemas.item_create_schema import ItemCreateSchema
from ..schemas.item_list_response_schema import ItemListResponseSchema
from ..schemas.item_schema import ItemSchema
from ..utils.request_base import RequestBase


class ItemsEndpoint:
    def __init__(self, request_base: RequestBase):
        """This class contains all methods that are available under endpoint `/items`."""

        self._request_base = request_base

    def get(self, headers: Dict = {}) -> ItemListResponseSchema:
        """List items

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.

        Returns:
            ItemListResponseSchema: The response returned by the endpoint.
        """
        response = self._request_base.get(
            uri="/items",
            headers={**headers},
            params={},
        )

        return ItemListResponseSchema(**response.json())

    def post(
        self,
        headers: Dict = {},
        content_type: Literal["application/json"] = "application/json",
        request_body: ItemCreateSchema = {},
    ) -> ItemSchema:
        """Create an item

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.
            - content_type (string): The content-type that is accepted by the API.
            - request_body (ItemCreateSchema): The requested body

        Returns:
            ItemSchema: The response returned by the endpoint.
        """
        response = self._request_base.post(
            uri="/items",
            headers={"Content-Type": content_type, **headers},
            params={},
            request_body=request_body.model_dump(),
        )

        return ItemSchema(**response.json())
