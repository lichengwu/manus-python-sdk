# Manus Python SDK

[![PyPI](https://img.shields.io/pypi/v/manus-sdk?color=blue)](https://pypi.org/project/manus-sdk/)
[![Python Versions](https://img.shields.io/pypi/pyversions/manus-sdk?color=blue)](https://pypi.org/project/manus-sdk/)
[![License](https://img.shields.io/pypi/l/manus-sdk?color=blue)](https://github.com/lichengwu/manus-python-sdk/blob/main/LICENSE)
[![CI](https://github.com/lichengwu/manus-python-sdk/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/lichengwu/manus-python-sdk/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/lichengwu/manus-python-sdk?color=green)](https://github.com/lichengwu/manus-python-sdk/releases)

> ⚠️ **Unofficial Community SDK** - This is a community-maintained Python SDK for the [Manus AI API](https://open.manus.im/docs). Not affiliated with or endorsed by Manus AI.

> 🎉 **v0.1.0** now available on PyPI! Install with `pip install manus-sdk`

## Features

- 🚀 **OpenAI SDK Compatible** - Use with the official OpenAI Python SDK (`openai>=1.100.2`)
- ⚡ **Async Support** - Full async/await support with `httpx`
- 📦 **Complete API Coverage** - Projects, Tasks, Files, Webhooks, Models
- 🔒 **Type Safe** - Full type hints with Pydantic models
- 🔄 **Streaming** - Server-sent events support
- 📄 **File Upload** - Presigned URL-based file upload
- 🔔 **Webhooks** - Webhook management and signature verification
- 🛠️ **Community Maintained** - Built by the community, for the community

## Installation

### From PyPI (Recommended)

```bash
pip install manus-sdk
```

### From GitHub Packages

```bash
pip install --index-url https://pypi.pkg.github.com/lichengwu/simple manus-sdk
```

### With Optional Dependencies

```bash
pip install "manus-sdk[all]"
```

## Quick Start

### Using OpenAI SDK (Recommended)

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.manus.im/v1",
    api_key="**",  # Placeholder
    default_headers={
        "API_KEY": "your-manus-api-key",
    },
)

# Create a task
response = client.responses.create(
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "What's the weather today?"}
            ],
        }
    ],
    extra_body={
        "task_mode": "agent",
        "agent_profile": "manus-1.6",
    },
)

print(f"Task created: {response.id}")
print(f"Status: {response.status}")
```

### Using Native SDK

```python
from manus import Manus

client = Manus(api_key="your-api-key")

# Create a task via Responses API
response = client.responses.create(
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Hello, world!"}
            ],
        }
    ],
    extra_body={
        "task_mode": "agent",
        "agent_profile": "manus-1.6",
    },
)

# List projects
projects = client.projects.list()

# Upload a file
file = client.files.create_and_upload(
    filename="document.pdf",
    file_content="/path/to/file.pdf",
)
```

## API Reference

### Tasks

Create and manage AI tasks:

```python
# Create a task
response = client.responses.create(
    input=[{"role": "user", "content": [{"type": "input_text", "text": "Hello"}]}],
    extra_body={"task_mode": "agent", "agent_profile": "manus-1.6"},
)

# Get task status
task = client.get(f"/tasks/{task_id}", cast_to=object)

# List tasks
tasks = client.get("/v1/tasks", cast_to=object)
```

### Projects

Organize tasks into projects:

```python
# Create a project
project = client.projects.create(
    name="My Project",
    description="Project description",
    instruction="Default instruction for all tasks",
)

# List projects
projects = client.projects.list()

# Get a project
project = client.projects.retrieve(project_id)

# Update a project
project = client.projects.update(
    project_id,
    name="New Name",
    description="Updated description",
)

# Delete a project
client.projects.delete(project_id)
```

### Files

Upload and manage files:

```python
# Create file record and upload in one step
file = client.files.create_and_upload(
    filename="document.pdf",
    file_content="/path/to/file.pdf",
    purpose="assistants",
)

# Or create and upload separately
file_record = client.files.create(filename="document.pdf")
client.files.upload(file_record.id, file_content, file_record.upload_url)

# List files
files = client.files.list()

# Get file details
file = client.files.retrieve(file_id)

# Delete a file
client.files.delete(file_id)
```

### Webhooks

Manage webhook subscriptions:

```python
# Create a webhook
webhook = client.webhooks.create(
    url="https://your-server.com/webhook",
    events=["task.created", "task.completed", "task.failed"],
)

# List webhooks
webhooks = client.webhooks.list()

# Verify webhook signature
from manus import Webhooks

is_valid = Webhooks.verify_signature(
    payload=request.body,
    signature=request.headers["X-Manus-Signature"],
    secret="your-webhook-secret",
)
```

## Async Usage

```python
import asyncio
from manus import AsyncManus

async def main():
    client = AsyncManus(api_key="your-api-key")
    
    # Create a task
    response = await client.responses.create(
        input=[{"role": "user", "content": [{"type": "input_text", "text": "Hello"}]}],
        extra_body={"task_mode": "agent", "agent_profile": "manus-1.6"},
    )
    
    # List projects
    projects = await client.projects.list()
    
    await client.close()

asyncio.run(main())
```

## Streaming

```python
from manus import Manus

client = Manus(api_key="your-api-key")

# Streaming response
stream = client.chat.completions.create(
    model="manus-v1",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

## Error Handling

```python
from manus import Manus, APIError, RateLimitError, AuthenticationError

client = Manus(api_key="your-api-key")

try:
    response = client.responses.create(...)
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except RateLimitError as e:
    print(f"Rate limited: {e}")
except APIError as e:
    print(f"API error: {e.status_code} - {e}")
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MANUS_API_KEY` | Your Manus API key | - |
| `MANUS_BASE_URL` | API base URL | `https://api.manus.ai/v1` |

### Client Options

```python
client = Manus(
    api_key="your-api-key",
    base_url="https://api.manus.im/v1",
    timeout=600.0,  # 10 minutes
    max_retries=3,
    default_headers={"X-Custom-Header": "value"},
)
```

## Task Statuses

| Status | Description |
|--------|-------------|
| `running` | Task is being processed |
| `pending` | Waiting for user input |
| `completed` | Task finished successfully |
| `error` | Task failed |

## File Management

- Uploaded files are automatically deleted after **48 hours**
- Presigned upload URLs expire after **3 minutes**
- Supported formats: PDF, DOCX, TXT, MD, CSV, XLSX, images, code files

## Examples

See the [`examples/`](examples/) directory for complete examples:

- [`basic_usage.py`](examples/basic_usage.py) - Basic task creation
- [`async_example.py`](examples/async_example.py) - Async usage
- [`streaming.py`](examples/streaming.py) - Streaming responses
- [`chat_completion.py`](examples/chat_completion.py) - Chat completions
- [`file_upload.py`](examples/file_upload.py) - File upload
- [`webhooks.py`](examples/webhooks.py) - Webhook management

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/lichengwu/manus-python-sdk.git
cd manus-python-sdk

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=manus --cov-report=html

# Run specific test file
pytest tests/test_client.py
```

### Linting

```bash
# Run ruff
ruff check src/manus tests

# Run mypy
mypy src/manus
```

## Contributing

1. Fork the repository: https://github.com/lichengwu/manus-python-sdk/fork
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request: https://github.com/lichengwu/manus-python-sdk/compare

## License

[MIT License](LICENSE)

## Disclaimer

This is an **unofficial community-maintained SDK** and is not affiliated with, endorsed by, or sponsored by Manus AI. The SDK is provided "as is" without warranty of any kind. Use at your own risk.

For official Manus AI documentation and support, please visit:
- Official Documentation: https://open.manus.im/docs
- Official API Reference: https://open.manus.im/docs/api-reference

## Support

- 📖 This SDK Docs: https://github.com/lichengwu/manus-python-sdk#readme
- 🐛 SDK Issues: https://github.com/lichengwu/manus-python-sdk/issues
- 📦 PyPI: https://pypi.org/project/manus-sdk/
- 💬 Discussions: https://github.com/lichengwu/manus-python-sdk/discussions

### Official Manus Resources

- 🌐 Official Documentation: https://open.manus.im/docs
- 📚 Official API Reference: https://open.manus.im/docs/api-reference
