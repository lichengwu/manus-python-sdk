"""Asynchronous client for the Manus Python SDK."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Dict, Optional, Type

import httpx

from ._streaming import AsyncStream
from ._types import RequestOptions
from ._utils import get_env_var, merge_headers, parse_timeout
from .exceptions import (
    APIConnectionError,
    APIResponseValidationError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)
from .resources import Chat, Files, Models, Projects, Webhooks


class AsyncManus:
    """Asynchronous client for the Manus API."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        default_headers: Optional[Mapping[str, str]] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        """Initialize the AsyncManus client.

        Args:
            api_key: API key for authentication. If not provided, will be read from
                the MANUS_API_KEY environment variable.
            base_url: Base URL for the API. If not provided, defaults to
                https://api.manus.ai/v1.
            timeout: Timeout for requests in seconds. Defaults to 600 (10 minutes).
            max_retries: Maximum number of retries for failed requests. Defaults to 3.
            default_headers: Default headers to include in all requests.
            http_client: Optional httpx.AsyncClient to use for requests. If not provided,
                a new client will be created.
        """
        # API key
        self.api_key = api_key or get_env_var("MANUS_API_KEY")
        if self.api_key is None:
            # For development, allow missing API key
            pass

        # Base URL
        self.base_url = base_url or get_env_var(
            "MANUS_BASE_URL",
            "https://api.manus.ai/v1",
        )

        # Timeout
        self.timeout = parse_timeout(timeout)

        # Max retries
        self.max_retries = max_retries

        # Default headers
        self._default_headers = self._prepare_headers(default_headers)

        # HTTP client
        self._client = http_client

        # Resources
        self.chat = Chat(self)
        self.models = Models(self)
        self.projects = Projects(self)
        self.files = Files(self)
        self.webhooks = Webhooks(self)

    def _prepare_headers(
        self, default_headers: Optional[Mapping[str, str]]
    ) -> Dict[str, str]:
        """Prepare the default headers."""
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        if default_headers:
            headers.update(default_headers)

        return headers

    def _build_headers(
        self,
        override_headers: Optional[Mapping[str, str]] = None,
    ) -> Dict[str, str]:
        """Build headers for a request."""
        return merge_headers(self._default_headers, override_headers)

    def _build_url(self, path: str) -> str:
        """Build a full URL from a path."""
        # Remove leading slash if present
        if path.startswith("/"):
            path = path[1:]
        return f"{self.base_url}/{path}"

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[float] = None,
        stream: bool = False,
    ) -> httpx.Response:
        """Make an HTTP request."""
        url = self._build_url(path)
        request_headers = self._build_headers(headers)

        client = self._client or httpx.AsyncClient(
            timeout=self.timeout,
            limits=httpx.Limits(max_keepalive_connections=100),
        )

        try:
            if stream:
                # For streaming, we need to use the client as a context manager
                if self._client is None:
                    async with httpx.AsyncClient(timeout=self.timeout) as client:
                        response = client.stream(
                            method,
                            url,
                            headers=request_headers,
                            params=params,
                            json=body,
                        )
                        return response
                else:
                    return self._client.stream(
                        method,
                        url,
                        headers=request_headers,
                        params=params,
                        json=body,
                    )
            else:
                response = await client.request(
                    method,
                    url,
                    headers=request_headers,
                    params=params,
                    json=body,
                    timeout=timeout,
                )
                return response
        except httpx.TimeoutException as e:
            raise APITimeoutError(
                message=f"Request timed out: {e}",
            ) from e
        except httpx.ConnectError as e:
            raise APIConnectionError(
                message=f"Failed to connect to API: {e}",
            ) from e
        except httpx.RequestError as e:
            raise APIConnectionError(
                message=f"Request failed: {e}",
            ) from e

    def _handle_response(self, response: httpx.Response) -> httpx.Response:
        """Handle an HTTP response, raising errors for non-success status codes."""
        if response.status_code < 200 or response.status_code >= 300:
            raise self._make_status_error(response)
        return response

    def _make_status_error(self, response: httpx.Response) -> APIStatusError:
        """Create an appropriate error for a failed response."""
        status_code = response.status_code
        request_id = response.headers.get("x-request-id")

        try:
            body = response.json()
            message = body.get("error", {}).get("message", str(body))
        except Exception:
            message = response.text or f"HTTP {status_code}"

        if status_code == 400:
            return BadRequestError(message, request_id=request_id, response=response)
        elif status_code == 401:
            return AuthenticationError(
                message, request_id=request_id, response=response
            )
        elif status_code == 403:
            return PermissionDeniedError(
                message, request_id=request_id, response=response
            )
        elif status_code == 404:
            return NotFoundError(message, request_id=request_id, response=response)
        elif status_code == 409:
            return ConflictError(message, request_id=request_id, response=response)
        elif status_code == 429:
            return RateLimitError(message, request_id=request_id, response=response)
        elif status_code >= 500:
            return InternalServerError(
                message, request_id=request_id, response=response
            )
        else:
            return APIStatusError(
                message, status_code=status_code, request_id=request_id, response=response
            )

    async def _get(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        cast_to: Type[Any],
        options: Optional[RequestOptions] = None,
    ) -> Any:
        """Make a GET request."""
        response = self._request(
            "GET",
            path,
            params=params,
            headers=options.get("headers") if options else None,
            timeout=options.get("timeout") if options else None,
        )
        self._handle_response(await response)
        return self._process_response(await response, cast_to)

    async def _post(
        self,
        path: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        cast_to: Type[Any],
        options: Optional[RequestOptions] = None,
    ) -> Any:
        """Make a POST request."""
        response = self._request(
            "POST",
            path,
            body=body,
            headers=options.get("headers") if options else None,
            timeout=options.get("timeout") if options else None,
        )
        self._handle_response(await response)
        return self._process_response(await response, cast_to)

    def _post_streaming(
        self,
        path: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        cast_to: Type[Any],
        options: Optional[RequestOptions] = None,
    ) -> AsyncStream[Any]:
        """Make a POST request with streaming response."""
        response = self._request(
            "POST",
            path,
            body=body,
            headers=options.get("headers") if options else None,
            timeout=options.get("timeout") if options else None,
            stream=True,
        )

        async def get_response() -> httpx.Response:
            resp = await response
            self._handle_response(resp)
            return resp

        # For streaming, we return the async stream directly
        # The actual request is made when iterating
        return AsyncStream(cast_to=cast_to, response=response, client=self)

    async def _delete(
        self,
        path: str,
        *,
        cast_to: Type[Any] = bool,
        options: Optional[RequestOptions] = None,
    ) -> Any:
        """Make a DELETE request."""
        response = self._request(
            "DELETE",
            path,
            headers=options.get("headers") if options else None,
            timeout=options.get("timeout") if options else None,
        )
        self._handle_response(await response)
        if cast_to is bool:
            resp = await response
            return resp.status_code == 200 or resp.status_code == 204
        return self._process_response(await response, cast_to)

    def _process_response(self, response: httpx.Response, cast_to: Type[Any]) -> Any:
        """Process a response, casting to the expected type."""
        try:
            data = response.json()
        except Exception as e:
            raise APIResponseValidationError(
                message=f"Failed to parse response as JSON: {e}",
                response=response,
            ) from e

        if cast_to is dict:
            return data
        elif hasattr(cast_to, "model_validate"):
            return cast_to.model_validate(data)
        else:
            return cast_to(**data)

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client is not None:
            await self._client.aclose()

    async def __aenter__(self) -> AsyncManus:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
