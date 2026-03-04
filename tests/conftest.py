"""Test configuration and fixtures for the Manus Python SDK."""

from __future__ import annotations

import os
from typing import Any, Dict, Generator, Optional

import pytest

from manus import AsyncManus, Manus


@pytest.fixture(scope="session")
def api_key() -> str:
    """Get the API key from environment or return a dummy key."""
    return os.environ.get("MANUS_API_KEY", "sk-test-key-for-testing")


@pytest.fixture(scope="session")
def base_url() -> str:
    """Get the base URL for testing."""
    return os.environ.get("MANUS_BASE_URL", "https://api.manus.ai/v1")


@pytest.fixture
def client(api_key: str, base_url: str) -> Generator[Manus, None, None]:
    """Create a synchronous test client."""
    client = Manus(api_key=api_key, base_url=base_url)
    yield client
    client.close()


@pytest.fixture
async def async_client(api_key: str, base_url: str) -> AsyncGenerator[AsyncManus, None]:
    """Create an asynchronous test client."""
    client = AsyncManus(api_key=api_key, base_url=base_url)
    yield client
    await client.close()


@pytest.fixture
def chat_messages() -> list[Dict[str, Any]]:
    """Sample chat messages for testing."""
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"},
    ]


@pytest.fixture
def completion_response() -> Dict[str, Any]:
    """Sample chat completion response."""
    return {
        "id": "chatcmpl-test123",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "manus-v1",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Hello! I'm doing well, thank you for asking.",
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 12,
            "total_tokens": 22,
        },
    }


@pytest.fixture
def models_response() -> Dict[str, Any]:
    """Sample models list response."""
    return {
        "object": "list",
        "data": [
            {
                "id": "manus-v1",
                "object": "model",
                "created": 1234567890,
                "owned_by": "manus",
                "name": "Manus V1",
                "description": "The flagship Manus model",
            },
            {
                "id": "manus-lite",
                "object": "model",
                "created": 1234567890,
                "owned_by": "manus",
                "name": "Manus Lite",
                "description": "A lightweight version of Manus",
            },
        ],
        "has_more": False,
    }


@pytest.fixture
def model_response() -> Dict[str, Any]:
    """Sample single model response."""
    return {
        "id": "manus-v1",
        "object": "model",
        "created": 1234567890,
        "owned_by": "manus",
        "name": "Manus V1",
        "description": "The flagship Manus model",
        "context_window": 128000,
    }


@pytest.fixture
def error_response() -> Dict[str, Any]:
    """Sample error response."""
    return {
        "error": {
            "message": "Invalid API key provided",
            "type": "invalid_request_error",
            "code": "invalid_api_key",
        }
    }
