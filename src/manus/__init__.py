"""Manus Python SDK - Official client for the Manus AI API.

The Manus API allows you to integrate AI agents into your workflows.
This SDK provides both synchronous and asynchronous clients with full type support.

Example:
    >>> from manus import Manus
    >>> client = Manus(api_key="your-api-key")
    >>> response = client.responses.create(
    ...     input=[{"role": "user", "content": [{"type": "input_text", "text": "Hello"}]}],
    ...     extra_body={"task_mode": "agent", "agent_profile": "manus-1.6"},
    ... )
    >>> print(f"Task created: {response.id}")

For more information, see:
    - Documentation: https://open.manus.im/docs
    - API Reference: https://open.manus.im/docs/api-reference
"""

from . import _version
from ._streaming import AsyncStream, Stream
from ._types import (
    ChatCompletionChunkChoiceDelta,
    ChatMessage,
    CompletionChoice,
    CompletionUsage,
    JSONArray,
    JSONObject,
    JSONValue,
    ModelInfo,
    RequestOptions,
)
from .async_client import AsyncManus
from .client import Manus
from .exceptions import (
    APIConnectionError,
    APIError,
    APIResponseValidationError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    InternalServerError,
    ManusError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)
from .pagination import (
    AsyncCursorPage,
    CursorPage,
)
from .resources import (
    Chat,
    ChatCompletions,
    FileObject,
    Files,
    Model,
    Models,
    Project,
    Projects,
    Webhook,
    Webhooks,
)
from .resources.chat import (
    ChatCompletion,
    ChatCompletionChoice,
    ChatCompletionChunk,
    ChatCompletionMessage,
)

__version__ = _version.VERSION

__all__ = [
    # Clients
    "Manus",
    "AsyncManus",
    # Resources
    "Chat",
    "ChatCompletions",
    "Models",
    "Projects",
    "Files",
    "Webhooks",
    # Response types
    "ChatCompletion",
    "ChatCompletionChoice",
    "ChatCompletionChunk",
    "ChatCompletionMessage",
    "ChatCompletionChunkChoiceDelta",
    "Model",
    "ModelInfo",
    "Project",
    "FileObject",
    "Webhook",
    # Streaming
    "Stream",
    "AsyncStream",
    # Pagination
    "CursorPage",
    "AsyncCursorPage",
    # Types
    "ChatMessage",
    "CompletionUsage",
    "CompletionChoice",
    "RequestOptions",
    "JSONObject",
    "JSONArray",
    "JSONValue",
    # Exceptions
    "ManusError",
    "APIError",
    "APIConnectionError",
    "APITimeoutError",
    "APIStatusError",
    "APIResponseValidationError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "RateLimitError",
    "InternalServerError",
    # Version
    "__version__",
]
