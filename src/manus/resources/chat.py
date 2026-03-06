"""Chat Completions API resource."""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Union,
    overload,
)

from pydantic import BaseModel, ConfigDict

from .._streaming import AsyncStream, ChatCompletionChunk, Stream
from .._types import ChatMessage, CompletionUsage

if TYPE_CHECKING:
    from ..async_client import AsyncManus
    from ..client import Manus


class ChatCompletionMessage(BaseModel):
    """A chat completion message."""

    model_config = ConfigDict(extra="allow")

    role: str
    content: Optional[str] = None
    refusal: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None


class ChatCompletionChoice(BaseModel):
    """A choice in a chat completion response."""

    model_config = ConfigDict(extra="allow")

    index: int
    message: ChatCompletionMessage
    finish_reason: Optional[str] = None
    logprobs: Optional[Any] = None


class ChatCompletion(BaseModel):
    """A chat completion response."""

    model_config = ConfigDict(extra="allow")

    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Optional[CompletionUsage] = None
    system_fingerprint: Optional[str] = None


class ChatCompletionChunkChoice(BaseModel):
    """A choice in a chat completion chunk."""

    model_config = ConfigDict(extra="allow")

    index: int
    delta: Dict[str, Any]
    finish_reason: Optional[str] = None


class ChatCompletions:
    """Chat Completions API resource."""

    def __init__(self, client: Union[Manus, AsyncManus]) -> None:
        self._client = client

    @overload
    def create(
        self,
        *,
        messages: List[Union[ChatMessage, Dict[str, Any]]],
        model: str,
        frequency_penalty: Optional[float] = None,
        logit_bias: Optional[Dict[str, int]] = None,
        logprobs: Optional[bool] = None,
        max_tokens: Optional[int] = None,
        presence_penalty: Optional[float] = None,
        response_format: Optional[Dict[str, Any]] = None,
        seed: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: Literal[False] = False,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        user: Optional[str] = None,
        **kwargs: Any,
    ) -> ChatCompletion:
        """Create a chat completion (non-streaming)."""
        ...

    @overload
    def create(
        self,
        *,
        messages: List[Union[ChatMessage, Dict[str, Any]]],
        model: str,
        frequency_penalty: Optional[float] = None,
        logit_bias: Optional[Dict[str, int]] = None,
        logprobs: Optional[bool] = None,
        max_tokens: Optional[int] = None,
        presence_penalty: Optional[float] = None,
        response_format: Optional[Dict[str, Any]] = None,
        seed: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: Literal[True],
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        user: Optional[str] = None,
        **kwargs: Any,
    ) -> Stream[ChatCompletionChunk]:
        """Create a chat completion (streaming)."""
        ...

    def create(
        self,
        *,
        messages: List[Union[ChatMessage, Dict[str, Any]]],
        model: str,
        frequency_penalty: Optional[float] = None,
        logit_bias: Optional[Dict[str, int]] = None,
        logprobs: Optional[bool] = None,
        max_tokens: Optional[int] = None,
        presence_penalty: Optional[float] = None,
        response_format: Optional[Dict[str, Any]] = None,
        seed: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        user: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[ChatCompletion, Stream[ChatCompletionChunk]]:
        """Create a chat completion."""

        is_async = type(self._client).__name__ == "AsyncManus"

        body = {
            "messages": messages,
            "model": model,
            **kwargs,
        }

        # Add optional parameters
        if frequency_penalty is not None:
            body["frequency_penalty"] = frequency_penalty
        if logit_bias is not None:
            body["logit_bias"] = logit_bias
        if logprobs is not None:
            body["logprobs"] = logprobs
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if presence_penalty is not None:
            body["presence_penalty"] = presence_penalty
        if response_format is not None:
            body["response_format"] = response_format
        if seed is not None:
            body["seed"] = seed
        if stop is not None:
            body["stop"] = stop
        if temperature is not None:
            body["temperature"] = temperature
        if top_p is not None:
            body["top_p"] = top_p
        if tools is not None:
            body["tools"] = tools
        if tool_choice is not None:
            body["tool_choice"] = tool_choice
        if user is not None:
            body["user"] = user

        if stream:
            if is_async:
                return self._client._post_streaming(  # type: ignore
                    "/chat/completions",
                    body=body,
                    cast_to=ChatCompletionChunk,
                )
            else:
                return self._client._post_streaming(
                    "/chat/completions",
                    body=body,
                    cast_to=ChatCompletionChunk,
                )
        else:
            if is_async:
                import asyncio

                return asyncio.get_event_loop().run_until_complete(
                    self._client._post(  # type: ignore
                        "/chat/completions",
                        body=body,
                        cast_to=ChatCompletion,
                    )
                )
            else:
                return self._client._post(
                    "/chat/completions",
                    body=body,
                    cast_to=ChatCompletion,
                )

    @overload
    async def create_async(
        self,
        *,
        messages: List[Union[ChatMessage, Dict[str, Any]]],
        model: str,
        frequency_penalty: Optional[float] = None,
        logit_bias: Optional[Dict[str, int]] = None,
        logprobs: Optional[bool] = None,
        max_tokens: Optional[int] = None,
        presence_penalty: Optional[float] = None,
        response_format: Optional[Dict[str, Any]] = None,
        seed: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: Literal[False] = False,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        user: Optional[str] = None,
        **kwargs: Any,
    ) -> ChatCompletion:
        """Create a chat completion asynchronously (non-streaming)."""
        ...

    @overload
    async def create_async(
        self,
        *,
        messages: List[Union[ChatMessage, Dict[str, Any]]],
        model: str,
        frequency_penalty: Optional[float] = None,
        logit_bias: Optional[Dict[str, int]] = None,
        logprobs: Optional[bool] = None,
        max_tokens: Optional[int] = None,
        presence_penalty: Optional[float] = None,
        response_format: Optional[Dict[str, Any]] = None,
        seed: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: Literal[True],
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        user: Optional[str] = None,
        **kwargs: Any,
    ) -> AsyncStream[ChatCompletionChunk]:
        """Create a chat completion asynchronously (streaming)."""
        ...

    async def create_async(
        self,
        *,
        messages: List[Union[ChatMessage, Dict[str, Any]]],
        model: str,
        frequency_penalty: Optional[float] = None,
        logit_bias: Optional[Dict[str, int]] = None,
        logprobs: Optional[bool] = None,
        max_tokens: Optional[int] = None,
        presence_penalty: Optional[float] = None,
        response_format: Optional[Dict[str, Any]] = None,
        seed: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        user: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[ChatCompletion, AsyncStream[ChatCompletionChunk]]:
        """Create a chat completion asynchronously."""

        body = {
            "messages": messages,
            "model": model,
            **kwargs,
        }

        # Add optional parameters
        if frequency_penalty is not None:
            body["frequency_penalty"] = frequency_penalty
        if logit_bias is not None:
            body["logit_bias"] = logit_bias
        if logprobs is not None:
            body["logprobs"] = logprobs
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if presence_penalty is not None:
            body["presence_penalty"] = presence_penalty
        if response_format is not None:
            body["response_format"] = response_format
        if seed is not None:
            body["seed"] = seed
        if stop is not None:
            body["stop"] = stop
        if temperature is not None:
            body["temperature"] = temperature
        if top_p is not None:
            body["top_p"] = top_p
        if tools is not None:
            body["tools"] = tools
        if tool_choice is not None:
            body["tool_choice"] = tool_choice
        if user is not None:
            body["user"] = user

        if stream:
            return self._client._post_streaming(
                "/chat/completions",
                body=body,
                cast_to=ChatCompletionChunk,
            )
        else:
            return await self._client._post(
                "/chat/completions",
                body=body,
                cast_to=ChatCompletion,
            )


class Chat:
    """Chat API resource."""

    def __init__(self, client: Union[Manus, AsyncManus]) -> None:
        self._client = client
        self.completions = ChatCompletions(client)
