"""Utility functions for the Manus Python SDK."""

from __future__ import annotations

import asyncio
import os
import time
from typing import Any, Callable, Coroutine, Dict, Mapping, Optional, TypeVar, overload

import httpx

T = TypeVar("T")


def get_env_var(name: str, default: Optional[str] = None) -> Optional[str]:
    """Get an environment variable."""
    return os.environ.get(name, default)


def get_required_env_var(name: str, *, description: Optional[str] = None) -> str:
    """Get a required environment variable, raising an error if not set."""
    value = os.environ.get(name)
    if value is None:
        desc = description or name
        raise ValueError(
            f"Environment variable {desc} is required. "
            f"Please set it using: export {name}=<your-{name.lower()}>",
        )
    return value


def parse_timeout(timeout: Optional[float]) -> float:
    """Parse a timeout value, ensuring it's positive."""
    if timeout is None:
        return 600.0  # Default 10 minutes
    if timeout <= 0:
        raise ValueError("Timeout must be a positive number")
    return float(timeout)


def merge_headers(
    base_headers: Mapping[str, str],
    override_headers: Optional[Mapping[str, str]],
) -> Dict[str, str]:
    """Merge two header dictionaries, with override taking precedence."""
    if not override_headers:
        return dict(base_headers)
    merged = dict(base_headers)
    merged.update(override_headers)
    return merged


@overload
def maybe_await(value: None) -> None: ...


@overload
def maybe_await(value: Coroutine[Any, Any, T]) -> T: ...


@overload
def maybe_await(value: T) -> T: ...


def maybe_await(
    value: Optional[Coroutine[Any, Any, T]] | T,
) -> Optional[T]:
    """Await a coroutine if provided, otherwise return the value."""
    if asyncio.iscoroutine(value):
        return asyncio.get_event_loop().run_until_complete(value)  # type: ignore[return-value]
    return value  # type: ignore[return-value]


def is_streaming_response(response: httpx.Response) -> bool:
    """Check if a response is a streaming response."""
    content_type = response.headers.get("content-type", "")
    return "text/event-stream" in content_type or "application/x-ndjson" in content_type


class retry_with_exponential_backoff:
    """Decorator for retrying functions with exponential backoff."""

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 0.5,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
    ) -> None:
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter

    def __call__(
        self,
        func: Callable[..., T],
    ) -> Callable[..., T]:
        """Wrap the function with retry logic."""

        def wrapper(*args: Any, **kwargs: Any) -> T:
            delay = self.initial_delay
            last_exception = None

            for attempt in range(self.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt == self.max_retries:
                        break

                    # Check if it's a retryable error
                    if not self._is_retryable_error(e):
                        raise

                    # Wait before retrying
                    actual_delay = delay
                    if self.jitter:
                        import random

                        actual_delay = delay * (0.5 + random.random())

                    time.sleep(actual_delay)
                    delay = min(delay * self.exponential_base, self.max_delay)

            if last_exception:
                raise last_exception
            raise RuntimeError("Unexpected retry loop exit")

        return wrapper

    def _is_retryable_error(self, error: Exception) -> bool:
        """Check if an error is retryable."""
        from .exceptions import APIConnectionError, APITimeoutError, APIStatusError

        if isinstance(error, (APIConnectionError, APITimeoutError)):
            return True

        if isinstance(error, APIStatusError):
            # Retry on 5xx and 429
            return error.status_code >= 500 or error.status_code == 429

        return False
