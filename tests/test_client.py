"""Tests for the synchronous Manus client."""

from __future__ import annotations

import os
from typing import Any
from unittest.mock import patch

import httpx
import pytest

from manus import (
    APITimeoutError,
    AuthenticationError,
    Manus,
    Model,
)


class TestManusClient:
    """Tests for the Manus client."""

    def test_client_init_default(self) -> None:
        """Test client initialization with default settings."""
        client = Manus(api_key="test-key")
        assert client.api_key == "test-key"
        assert client.base_url == "https://api.manus.ai/v1"
        assert client.timeout == 600.0
        assert client.max_retries == 3

    def test_client_init_custom(self) -> None:
        """Test client initialization with custom settings."""
        client = Manus(
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
            client = Manus()
            assert client.api_key == "env-key"
            assert client.base_url == "https://env.api.com/v1"

    def test_client_context_manager(self) -> None:
        """Test client as context manager."""
        with Manus(api_key="test-key") as client:
            assert client.api_key == "test-key"
        # Client should be closed after exiting context

    def test_build_headers(self) -> None:
        """Test header building."""
        client = Manus(api_key="test-key")
        headers = client._build_headers()
        assert headers["Authorization"] == "Bearer test-key"
        assert headers["Content-Type"] == "application/json"
        assert headers["Accept"] == "application/json"

    def test_build_headers_override(self) -> None:
        """Test header building with override."""
        client = Manus(api_key="test-key")
        headers = client._build_headers({"X-Custom": "value"})
        assert headers["Authorization"] == "Bearer test-key"
        assert headers["X-Custom"] == "value"

    def test_build_url(self) -> None:
        """Test URL building."""
        client = Manus(api_key="test-key")
        assert client._build_url("/chat/completions") == "https://api.manus.ai/v1/chat/completions"
        assert client._build_url("models") == "https://api.manus.ai/v1/models"

    def test_build_url_custom_base(self) -> None:
        """Test URL building with custom base."""
        client = Manus(api_key="test-key", base_url="https://custom.api.com/v2")
        assert client._build_url("/chat") == "https://custom.api.com/v2/chat"


class TestManusChat:
    """Tests for the Chat API."""

    @pytest.fixture
    def mock_response(self) -> httpx.Response:
        """Create a mock HTTP response."""
        return httpx.Response(
            status_code=200,
            json={
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
            },
        )

    def test_chat_create_mock(self, client: Manus, mock_response: httpx.Response) -> None:
        """Test chat completion creation with mocked response."""
        with patch.object(client, "_post", return_value=mock_response.json()) as mock_post:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": "Hello"}],
                model="manus-v1",
            )
            assert mock_post.called
            assert response is not None

    def test_chat_create_with_options(self, client: Manus) -> None:
        """Test chat completion with various options."""
        # Just verify the method accepts the options without error
        # Actual API call would require a real server
        with patch.object(client, "_post", return_value={"id": "test"}):
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": "Hello"}],
                model="manus-v1",
                temperature=0.7,
                max_tokens=100,
                top_p=0.9,
            )
            assert response is not None


class TestManusModels:
    """Tests for the Models API."""

    def test_models_list_mock(self, client: Manus) -> None:
        """Test models list with mocked response."""
        mock_data = {
            "object": "list",
            "data": [{"id": "manus-v1", "object": "model"}],
            "has_more": False,
        }
        with patch.object(client, "_get", return_value=mock_data) as mock_get:
            response = client.models.list()
            assert mock_get.called
            assert response is not None

    def test_models_retrieve_mock(self, client: Manus) -> None:
        """Test model retrieval with mocked response."""
        mock_data = {"id": "manus-v1", "object": "model", "name": "Test Model"}
        with patch.object(client, "_get", return_value=mock_data) as mock_get:
            response = client.models.retrieve("manus-v1")
            mock_get.assert_called_once_with(
                "/models/manus-v1",
                cast_to=Model,
            )
            assert response is not None


class TestManusErrors:
    """Tests for error handling."""

    def test_timeout_error(self) -> None:
        """Test timeout error handling."""
        client = Manus(api_key="test-key")

        def raise_timeout(*args: Any, **kwargs: Any) -> None:
            raise APITimeoutError("Request timed out")

        with patch.object(client, "_request", side_effect=raise_timeout):
            with pytest.raises(APITimeoutError):
                client._get("/test", cast_to=dict)

    def test_auth_error(self, client: Manus) -> None:
        """Test authentication error handling."""
        response = httpx.Response(
            status_code=401,
            json={"error": {"message": "Invalid API key"}},
        )
        error = client._make_status_error(response)
        assert isinstance(error, AuthenticationError)
        assert error.status_code == 401
