# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest                    # All tests
pytest tests/test_client.py  # Single test file

# Linting
ruff check src/manus tests
mypy src/manus
```

## Architecture Overview

**Package structure** (`src/manus/`):
- `client.py` / `async_client.py` - Synchronous and asynchronous HTTP clients using `httpx`
- `resources/*.py` - API resource modules (Chat, Files, Models, Projects, Webhooks) following the resource pattern
- `_streaming.py` - Streaming response handling
- `pagination.py` - Cursor-based pagination (`CursorPage`, `AsyncCursorPage`)
- `_types.py` - Type definitions (Pydantic models for API responses)
- `exceptions.py` - Hierarchical exception classes (`APIError`, `AuthenticationError`, `RateLimitError`, etc.)

**Key patterns**:
- Resources are instantiated with a client instance (e.g., `Projects(client)`)
- HTTP methods are private (`_get`, `_post`, `_delete`) and return raw responses
- Public methods on resources call private methods with `cast_to` for type-safe deserialization
- Environment variables: `MANUS_API_KEY`, `MANUS_BASE_URL`

## Testing

Tests use `pytest` with `pytest-asyncio` for async support. Mock `httpx.Response` objects and patch client methods (`_get`, `_post`) rather than making real API calls.
