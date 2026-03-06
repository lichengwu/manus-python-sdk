"""Tests for the asynchronous Manus client."""

from __future__ import annotations

import os
from typing import Any
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from manus import (
    APITimeoutError,
    AsyncManus,
    AuthenticationError,
    Model,
)


class TestAsyncManusClient:
    """Tests for the AsyncManus client."""

    def test_client_init_default(self) -> None:
        """Test client initialization with default settings."""
        client = AsyncManus(api_key="test-key")
        assert client.api_key == "test-key"
        assert client.base_url == "https://api.manus.ai/v1"
        assert client.timeout == 600.0
        assert client.max_retries == 3

    def test_client_init_custom(self) -> None:
        """Test client initialization with custom settings."""
        client = AsyncManus(
            api_key="test-key",
            base_url="https://custom.api.com/v1",
            timeout=30.0,
            max_retries=5,
        )
        assert client.api_key == "test-key"
        assert client.base_url == "https://custom.api.com/v1"
        assert client.timeout == 30.0
        assert client.max_retries == 5

    def test_client_init_from_env(self) -> None:
        """Test client initialization from environment variables."""
        with patch.dict(
            os.environ,
            {
                "MANUS_API_KEY": "env-key",
                "MANUS_BASE_URL": "https://env.api.com/v1",
            },
        ):
            client = AsyncManus()
            assert client.api_key == "env-key"
            assert client.base_url == "https://env.api.com/v1"

    @pytest.mark.asyncio
    async def test_client_context_manager(self) -> None:
        """Test client as async context manager."""
        async with AsyncManus(api_key="test-key") as client:
            assert client.api_key == "test-key"
        # Client should be closed after exiting context

    def test_build_headers(self) -> None:
        """Test header building."""
        client = AsyncManus(api_key="test-key")
        headers = client._build_headers()
        assert headers["Authorization"] == "Bearer test-key"
        assert headers["Content-Type"] == "application/json"
        assert headers["Accept"] == "application/json"

    def test_build_headers_override(self) -> None:
        """Test header building with override."""
        client = AsyncManus(api_key="test-key")
        headers = client._build_headers({"X-Custom": "value"})
        assert headers["Authorization"] == "Bearer test-key"
        assert headers["X-Custom"] == "value"

    def test_build_url(self) -> None:
        """Test URL building."""
        client = AsyncManus(api_key="test-key")
        assert client._build_url("/chat/completions") == "https://api.manus.ai/v1/chat/completions"
        assert client._build_url("models") == "https://api.manus.ai/v1/models"


class TestAsyncManusChat:
    """Tests for the async Chat API."""

    @pytest.mark.asyncio
    async def test_chat_create_async_mock(self, async_client: AsyncManus) -> None:
        """Test async chat completion creation with mocked response."""
        mock_data = {
            "id": "chatcmpl-test",
            "object": "chat.completion",
            "created": 1234567890,
            "model": "manus-v1",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "Hello!"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 3,
                "total_tokens": 8,
            },
        }
        with patch.object(
            async_client, "_post", new_callable=AsyncMock, return_value=mock_data
        ) as mock_post:
            response = await async_client.chat.completions.create_async(
                messages=[{"role": "user", "content": "Hello"}],
                model="manus-v1",
            )
            assert mock_post.called
            assert response is not None

    @pytest.mark.asyncio
    async def test_chat_create_async_with_options(self, async_client: AsyncManus) -> None:
        """Test async chat completion with various options."""
        mock_data = {"id": "test"}
        with patch.object(
            async_client, "_post", new_callable=AsyncMock, return_value=mock_data
        ):
            response = await async_client.chat.completions.create_async(
                messages=[{"role": "user", "content": "Hello"}],
                model="manus-v1",
                temperature=0.7,
                max_tokens=100,
                top_p=0.9,
            )
            assert response is not None


class TestAsyncManusModels:
    """Tests for the async Models API."""

    @pytest.mark.asyncio
    async def test_models_list_async_mock(self, async_client: AsyncManus) -> None:
        """Test async models list with mocked response."""
        mock_data = {
            "object": "list",
            "data": [{"id": "manus-v1", "object": "model"}],
            "has_more": False,
        }
        with patch.object(
            async_client, "_get", new_callable=AsyncMock, return_value=mock_data
        ) as mock_get:
            response = await async_client.models.list_async()
            assert mock_get.called
            assert response is not None

    @pytest.mark.asyncio
    async def test_models_retrieve_async_mock(self, async_client: AsyncManus) -> None:
        """Test async model retrieval with mocked response."""
        mock_data = {"id": "manus-v1", "object": "model", "name": "Test Model"}
        with patch.object(
            async_client, "_get", new_callable=AsyncMock, return_value=mock_data
        ) as mock_get:
            response = await async_client.models.retrieve_async("manus-v1")
            mock_get.assert_called_once_with(
                "/models/manus-v1",
                cast_to=Model,
                options=None,
            )
            assert response is not None

    @pytest.mark.asyncio
    async def test_models_delete_async_mock(self, async_client: AsyncManus) -> None:
        """Test async model deletion with mocked response."""
        with patch.object(
            async_client, "_delete", new_callable=AsyncMock, return_value=True
        ) as mock_delete:
            response = await async_client.models.delete_async("manus-v1")
            mock_delete.assert_called_once()
            assert response is True


class TestAsyncManusErrors:
    """Tests for async error handling."""

    @pytest.mark.asyncio
    async def test_timeout_error(self) -> None:
        """Test timeout error handling."""
        client = AsyncManus(api_key="test-key")

        async def raise_timeout(*args: Any, **kwargs: Any) -> httpx.Response:
            raise httpx.TimeoutException("Request timed out")

        with patch.object(client, "_request", side_effect=raise_timeout):
            with pytest.raises(APITimeoutError):
                await client._get("/test", cast_to=dict)

    def test_auth_error(self, async_client: AsyncManus) -> None:
        """Test authentication error handling."""
        response = httpx.Response(
            status_code=401,
            json={"error": {"message": "Invalid API key"}},
        )
        error = async_client._make_status_error(response)
        assert isinstance(error, AuthenticationError)
        assert error.status_code == 401
