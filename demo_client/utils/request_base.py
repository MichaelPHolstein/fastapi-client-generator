from typing import Any, Dict, Optional

from requests import Response, request


class HttpExceptionError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Error {status_code}: {detail}")


class RequestBase:
    def __init__(self, base_url: str, default_headers: Dict) -> None:
        self._base_url = base_url
        self._default_headers = default_headers

    def request(
        self,
        method: str,
        uri: str,
        request_body: Optional[Dict[str, Any]] = None,
        timeout: int = 15,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Response:
        """Generic request handler that supports all HTTP methods."""
        req_headers = {**self._default_headers, **(headers or {})}

        response = request(
            method=method.upper(),
            url=self._resolve_url(uri),
            headers=req_headers,
            json=request_body if request_body else None,
            timeout=timeout,
            params=params,
        )
        return self._handle_response(response)

    def get(self, uri: str, **kwargs) -> Response:
        return self.request("GET", uri, **kwargs)

    def post(self, uri: str, **kwargs) -> Response:
        return self.request("POST", uri, **kwargs)

    def put(self, uri: str, **kwargs) -> Response:
        return self.request("PUT", uri, **kwargs)

    def patch(self, uri: str, **kwargs) -> Response:
        return self.request("PATCH", uri, **kwargs)

    def delete(self, uri: str, **kwargs) -> Response:
        return self.request("DELETE", uri, **kwargs)

    def head(self, uri: str, **kwargs) -> Response:
        return self.request("HEAD", uri, **kwargs)

    def options(self, uri: str, **kwargs) -> Response:
        return self.request("OPTIONS", uri, **kwargs)

    def _resolve_url(self, uri: str) -> str:
        """Builds the full request URL."""
        return f"{self._base_url}/{uri.lstrip('/')}"

    def _handle_response(self, response: Response) -> Response:
        """Checks for HTTP errors and raises wrapped exception."""
        try:
            response.raise_for_status()
            return response
        except Exception:
            raise HttpExceptionError(
                status_code=response.status_code,
                detail=response.text,
            )
