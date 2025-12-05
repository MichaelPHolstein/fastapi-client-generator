from typing import Dict, Literal

from ..schemas.address_schema import AddressSchema
from ..utils.request_base import RequestBase


class AddressesEndpoint:
    def __init__(self, request_base: RequestBase):
        """This class contains all methods that are available under endpoint `/addresses`."""

        self._request_base = request_base

    def get(self, headers: Dict = {}) -> Dict:
        """Get your saved addresses

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.

        Returns:
            Dict: The response returned by the endpoint.
        """
        response = self._request_base.get(
            uri="/addresses",
            headers={**headers},
            params={},
        )

        return response.json()

    def post(
        self,
        headers: Dict = {},
        content_type: Literal["application/json"] = "application/json",
        request_body: AddressSchema = {},
    ) -> Dict:
        """Add a new address

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.
            - content_type (string): The content-type that is accepted by the API.
            - request_body (AddressSchema): The requested body

        Returns:
            Dict: The response returned by the endpoint.
        """
        response = self._request_base.post(
            uri="/addresses",
            headers={"Content-Type": content_type, **headers},
            params={},
            request_body=request_body.model_dump(),
        )

        return response.json()
