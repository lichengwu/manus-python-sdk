"""Tests for models and resources."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from manus import (
    ChatCompletion,
    ChatCompletionChoice,
    ChatCompletionChunk,
    ChatCompletionMessage,
    CompletionUsage,
    Model,
)
from manus._types import ModelInfo


class TestCompletionUsage:
    """Tests for CompletionUsage model."""

    def test_usage_creation(self) -> None:
        """Test CompletionUsage creation."""
        usage = CompletionUsage(
            prompt_tokens=10,
            completion_tokens=5,
            total_tokens=15,
        )
        assert usage.prompt_tokens == 10
        assert usage.completion_tokens == 5
        assert usage.total_tokens == 15

    def test_usage_validation(self) -> None:
        """Test CompletionUsage validation."""
        with pytest.raises(ValidationError):
            CompletionUsage(
                prompt_tokens="invalid",  # type: ignore
                completion_tokens=5,
                total_tokens=15,
            )


class TestChatCompletionMessage:
    """Tests for ChatCompletionMessage model."""

    def test_message_creation(self) -> None:
        """Test ChatCompletionMessage creation."""
        message = ChatCompletionMessage(
            role="assistant",
            content="Hello, world!",
        )
        assert message.role == "assistant"
        assert message.content == "Hello, world!"

    def test_message_with_tool_calls(self) -> None:
        """Test ChatCompletionMessage with tool calls."""
        tool_call = {
            "id": "call_123",
            "type": "function",
            "function": {"name": "get_weather", "arguments": '{"city": "NYC"}'},
        }
        message = ChatCompletionMessage(
            role="assistant",
            content=None,
            tool_calls=[tool_call],
        )
        assert message.role == "assistant"
        assert message.content is None
        assert message.tool_calls == [tool_call]


class TestChatCompletionChoice:
    """Tests for ChatCompletionChoice model."""

    def test_choice_creation(self) -> None:
        """Test ChatCompletionChoice creation."""
        message = ChatCompletionMessage(role="assistant", content="Hi!")
        choice = ChatCompletionChoice(
            index=0,
            message=message,
            finish_reason="stop",
        )
        assert choice.index == 0
        assert choice.message.role == "assistant"
        assert choice.finish_reason == "stop"


class TestChatCompletion:
    """Tests for ChatCompletion model."""

    def test_completion_creation(self) -> None:
        """Test ChatCompletion creation."""
        message = ChatCompletionMessage(role="assistant", content="Hello!")
        choice = ChatCompletionChoice(
            index=0,
            message=message,
            finish_reason="stop",
        )
        usage = CompletionUsage(prompt_tokens=5, completion_tokens=3, total_tokens=8)

        completion = ChatCompletion(
            id="chatcmpl-123",
            created=1234567890,
            model="manus-v1",
            choices=[choice],
            usage=usage,
        )

        assert completion.id == "chatcmpl-123"
        assert completion.object == "chat.completion"
        assert len(completion.choices) == 1
        assert completion.usage is not None
        assert completion.usage.total_tokens == 8

    def test_completion_from_dict(self) -> None:
        """Test ChatCompletion creation from dictionary."""
        data = {
            "id": "chatcmpl-123",
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
        completion = ChatCompletion.model_validate(data)
        assert completion.id == "chatcmpl-123"
        assert completion.choices[0].message.content == "Hello!"


class TestChatCompletionChunk:
    """Tests for ChatCompletionChunk model."""

    def test_chunk_creation(self) -> None:
        """Test ChatCompletionChunk creation."""
        chunk = ChatCompletionChunk(
            id="chatcmpl-chunk-123",
            created=1234567890,
            model="manus-v1",
            choices=[
                {
                    "index": 0,
                    "delta": {"role": "assistant", "content": "Hello"},
                    "finish_reason": None,
                }
            ],
        )
        assert chunk.id == "chatcmpl-chunk-123"
        assert chunk.choices[0].delta["content"] == "Hello"


class TestModel:
    """Tests for Model resource."""

    def test_model_creation(self) -> None:
        """Test Model creation."""
        model = Model(
            id="manus-v1",
            created=1234567890,
            owned_by="manus",
            name="Manus V1",
            description="The flagship Manus model",
        )
        assert model.id == "manus-v1"
        assert model.object == "model"
        assert model.owned_by == "manus"
        assert model.name == "Manus V1"

    def test_model_from_dict(self) -> None:
        """Test Model creation from dictionary."""
        data = {
            "id": "manus-lite",
            "object": "model",
            "created": 1234567890,
            "owned_by": "manus",
            "context_window": 128000,
        }
        model = Model.model_validate(data)
        assert model.id == "manus-lite"
        assert model.context_window == 128000

    def test_model_extra_fields(self) -> None:
        """Test Model accepts extra fields."""
        data = {
            "id": "manus-v1",
            "object": "model",
            "custom_field": "custom_value",
            "nested": {"key": "value"},
        }
        model = Model.model_validate(data)
        assert model.id == "manus-v1"
        # Extra fields are allowed
        assert model.custom_field == "custom_value"  # type: ignore


class TestModelInfo:
    """Tests for ModelInfo type."""

    def test_model_info_creation(self) -> None:
        """Test ModelInfo creation."""
        info = ModelInfo(
            id="manus-v1",
            created=1234567890,
            owned_by="manus",
        )
        assert info.id == "manus-v1"
        assert info.object == "model"
        assert info.owned_by == "manus"


class TestModelValidation:
    """Tests for model validation."""

    def test_invalid_usage(self) -> None:
        """Test validation with invalid usage data."""
        with pytest.raises(Exception):
            CompletionUsage(
                prompt_tokens=-1,  # Should be non-negative
                completion_tokens=5,
                total_tokens=15,
            )

    def test_minimal_completion(self) -> None:
        """Test minimal completion."""
        data = {
            "id": "chatcmpl-minimal",
            "created": 1234567890,
            "model": "manus-v1",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant"},
                    "finish_reason": None,
                }
            ],
        }
        completion = ChatCompletion.model_validate(data)
        assert completion.id == "chatcmpl-minimal"
        assert completion.choices[0].message.content is None
