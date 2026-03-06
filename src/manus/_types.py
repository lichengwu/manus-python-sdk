"""Type definitions for the Manus Python SDK."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Dict, List, Optional, TypeVar, Union

from pydantic import BaseModel, ConfigDict
from typing_extensions import NotRequired, Required, TypedDict

T = TypeVar("T")


class RequestOptions(TypedDict, total=False):
    """Options for individual requests."""

    headers: Optional[Mapping[str, str]]
    timeout: Optional[float]
    max_retries: Optional[int]


# API parameter types
JSONObject = Dict[str, Any]
JSONArray = List[Any]
JSONValue = Union[str, int, float, bool, None, JSONObject, JSONArray]


class CompletionUsage(BaseModel):
    """Usage information for completions."""

    model_config = ConfigDict(extra="allow")

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CompletionChoice(BaseModel):
    """A completion choice."""

    model_config = ConfigDict(extra="allow")

    index: int
    text: str
    logprobs: Optional[Any] = None
    finish_reason: Optional[str] = None


class ChatMessage(TypedDict, total=False):
    """A chat message."""

    role: Required[str]
    content: Required[Union[str, List[Dict[str, Any]]]]
    name: NotRequired[str]
    function_call: NotRequired[Dict[str, Any]]
    tool_calls: NotRequired[List[Dict[str, Any]]]
    tool_call_id: NotRequired[str]


class ChatCompletionChunkChoiceDelta(TypedDict, total=False):
    """Delta for a chat completion chunk choice."""

    role: str
    content: NotRequired[Optional[str]]
    function_call: NotRequired[Optional[Dict[str, Any]]]
    tool_calls: NotRequired[Optional[List[Dict[str, Any]]]]


class ModelInfo(BaseModel):
    """Information about a model."""

    model_config = ConfigDict(extra="allow")

    id: str
    object: str = "model"
    created: Optional[int] = None
    owned_by: Optional[str] = None
