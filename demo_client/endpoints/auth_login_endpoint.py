from typing import Dict, Literal

from ..utils.request_base import RequestBase


class AuthLoginEndpoint:
    def __init__(self, request_base: RequestBase):
        """This class contains all methods that are available under endpoint `/auth/login`."""

        self._request_base = request_base

    def post(
        self,
        headers: Dict = {},
        content_type: Literal["application/json"] = "application/json",
        request_body: Dict = {},
    ) -> Dict:
        """Login and get access token

        Args:
            - headers (Dict): HTTP headers that are specifically required for current API endpoint.
            - content_type (string): The content-type that is accepted by the API.
            - request_body (Dict[str, Any]): The requested body

        Returns:
            Dict: The response returned by the endpoint.
        """
        response = self._request_base.post(
            uri="/auth/login",
            headers={"Content-Type": content_type, **headers},
            params={},
            request_body=request_body,
        )

        return response.json()
