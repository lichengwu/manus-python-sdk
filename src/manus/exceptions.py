"""Exception classes for the Manus Python SDK."""

from __future__ import annotations

from typing import Any, Optional


class ManusError(Exception):
    """Base exception for all Manus SDK errors."""

    def __init__(self, message: str, *, request_id: Optional[str] = None) -> None:
        super().__init__(message)
        self.request_id = request_id


class APIError(ManusError):
    """Base class for API-related errors."""

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        request_id: Optional[str] = None,
    ) -> None:
        super().__init__(message, request_id=request_id)
        self.status_code = status_code


class APIConnectionError(APIError):
    """Error when failing to connect to the API."""

    def __init__(self, message: str, *, request_id: Optional[str] = None) -> None:
        super().__init__(message, status_code=None, request_id=request_id)


class APITimeoutError(APIConnectionError):
    """Error when the API request times out."""

    def __init__(self, message: str, *, request_id: Optional[str] = None) -> None:
        super().__init__(message, request_id=request_id)


class APIStatusError(APIError):
    """Error when the API returns an error status code."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        request_id: Optional[str] = None,
        response: Any = None,
    ) -> None:
        super().__init__(message, status_code=status_code, request_id=request_id)
        self.response = response


class BadRequestError(APIStatusError):
    """Error for 400 Bad Request responses."""

    def __init__(
        self,
        message: str,
        *,
        request_id: Optional[str] = None,
        response: Any = None,
    ) -> None:
        super().__init__(message, status_code=400, request_id=request_id, response=response)


class AuthenticationError(APIStatusError):
    """Error for 401 Unauthorized responses."""

    def __init__(
        self,
        message: str,
        *,
        request_id: Optional[str] = None,
        response: Any = None,
    ) -> None:
        super().__init__(message, status_code=401, request_id=request_id, response=response)


class PermissionDeniedError(APIStatusError):
    """Error for 403 Forbidden responses."""

    def __init__(
        self,
        message: str,
        *,
        request_id: Optional[str] = None,
        response: Any = None,
    ) -> None:
        super().__init__(message, status_code=403, request_id=request_id, response=response)


class NotFoundError(APIStatusError):
    """Error for 404 Not Found responses."""

    def __init__(
        self,
        message: str,
        *,
        request_id: Optional[str] = None,
        response: Any = None,
    ) -> None:
        super().__init__(message, status_code=404, request_id=request_id, response=response)


class ConflictError(APIStatusError):
    """Error for 409 Conflict responses."""

    def __init__(
        self,
        message: str,
        *,
        request_id: Optional[str] = None,
        response: Any = None,
    ) -> None:
        super().__init__(message, status_code=409, request_id=request_id, response=response)


class RateLimitError(APIStatusError):
    """Error for 429 Rate Limit responses."""

    def __init__(
        self,
        message: str,
        *,
        request_id: Optional[str] = None,
        response: Any = None,
    ) -> None:
        super().__init__(message, status_code=429, request_id=request_id, response=response)


class InternalServerError(APIStatusError):
    """Error for 500 Internal Server Error responses."""

    def __init__(
        self,
        message: str,
        *,
        request_id: Optional[str] = None,
        response: Any = None,
    ) -> None:
        super().__init__(message, status_code=500, request_id=request_id, response=response)


class APIResponseValidationError(ManusError):
    """Error when the API response fails validation."""

    def __init__(
        self,
        message: str,
        *,
        request_id: Optional[str] = None,
        response: Any = None,
    ) -> None:
        super().__init__(message, request_id=request_id)
        self.response = response
