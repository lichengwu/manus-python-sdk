"""Streaming support for the Manus Python SDK."""

from __future__ import annotations

import json
import re
from collections.abc import AsyncIterator, Iterator
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    List,
    Optional,
    TypeVar,
)

import httpx
from pydantic import BaseModel

from ._types import CompletionUsage

if TYPE_CHECKING:
    pass

T = TypeVar("T")

# SSE event pattern
SSEResponse = re.compile(b"event: (.*)?\\r?\\n")
SSEData = re.compile(b"data: (.*)?\\r?\\n")


class ServerSentEvent:
    """A server-sent event."""

    def __init__(self, *, event: Optional[str] = None, data: str = "") -> None:
        self.event = event
        self.data = data

    def __repr__(self) -> str:
        return f"ServerSentEvent(event={self.event!r}, data={self.data!r})"


class Stream(Generic[T]):
    """Iterator for SSE stream responses."""

    def __init__(
        self,
        *,
        cast_to: type[T],
        response: httpx.Response,
        client: Any,
    ) -> None:
        self._cast_to = cast_to
        self._response = response
        self._client = client
        self._iterator = self.__stream__()
        self._exhausted = False

    def __next__(self) -> T:
        return next(self._iterator)

    def __iter__(self) -> Iterator[T]:
        for item in self._iterator:
            yield item

    def _iter_lines(self) -> Iterator[str]:
        """Iterate over lines in the response."""
        for line in self._response.iter_lines():
            # Skip empty lines and comments
            if not line or line.startswith(":"):
                continue
            yield line

    def __stream__(self) -> Iterator[T]:
        """Stream the response."""
        data = ""

        for line in self._iter_lines():
            if line.startswith("data:"):
                data = line[5:].strip()

                # Empty data line means end of stream
                if data == "[DONE]":
                    return

                # Parse the data
                try:
                    parsed_data = json.loads(data)
                    # Cast to the expected type
                    if self._cast_to is dict:
                        yield parsed_data  # type: ignore
                    elif issubclass(self._cast_to, BaseModel):
                        yield self._cast_to.model_validate(parsed_data)  # type: ignore
                    else:
                        yield parsed_data
                except json.JSONDecodeError:
                    # If we can't parse as JSON, yield the raw data
                    yield data  # type: ignore

                # Reset for next event
                data = ""

    def close(self) -> None:
        """Close the response."""
        self._response.close()


class AsyncStream(Generic[T]):
    """Async iterator for SSE stream responses."""

    def __init__(
        self,
        *,
        cast_to: type[T],
        response: httpx.Response,
        client: Any,
    ) -> None:
        self._cast_to = cast_to
        self._response = response
        self._client = client
        self._exhausted = False

    async def __anext__(self) -> T:
        async for line in self._response.aiter_lines():
            # Skip empty lines and comments
            if not line or line.startswith(":"):
                continue

            if line.startswith("data:"):
                data = line[5:].strip()

                # Empty data line means end of stream
                if data == "[DONE]":
                    raise StopAsyncIteration

                # Parse the data
                try:
                    parsed_data = json.loads(data)
                    # Cast to the expected type
                    if self._cast_to is dict:
                        return parsed_data  # type: ignore
                    elif issubclass(self._cast_to, BaseModel):
                        return self._cast_to.model_validate(parsed_data)  # type: ignore
                    else:
                        return parsed_data
                except json.JSONDecodeError:
                    # If we can't parse as JSON, yield the raw data
                    return data  # type: ignore

        raise StopAsyncIteration

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def close(self) -> None:
        """Close the response."""
        await self._response.aclose()


class StreamedResponse(BaseModel):
    """Base class for streamed responses."""

    model_config = {"extra": "allow"}

    id: Optional[str] = None
    object: Optional[str] = None
    created: Optional[int] = None
    model: Optional[str] = None


class ChatCompletionChunk(StreamedResponse):
    """A chat completion chunk from a streaming response."""

    class Choice(BaseModel):
        """A choice in a chat completion chunk."""

        model_config = {"extra": "allow"}

        index: int
        delta: Dict[str, Any]
        finish_reason: Optional[str] = None

    choices: List[Choice]
    usage: Optional[CompletionUsage] = None
