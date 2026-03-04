"""Basic usage example for the Manus Python SDK."""

import os

from manus import Manus

# Create a client
# The API key is read from the MANUS_API_KEY environment variable by default
client = Manus(
    api_key=os.environ.get("MANUS_API_KEY"),
    # base_url="https://api.manus.ai/v1",  # Optional: custom base URL
    # timeout=600,  # Optional: request timeout in seconds
)

# Create a chat completion
response = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"},
    ],
    model="manus-v1",
)

# Access the response
print(f"Response ID: {response.id}")
print(f"Model: {response.model}")
print(f"Content: {response.choices[0].message.content}")
print(f"Usage: {response.usage}")

# List available models
models = client.models.list()
print(f"\nAvailable models: {[m.id for m in models.data]}")

# Retrieve a specific model
model = client.models.retrieve("manus-v1")
print(f"\nModel details: {model.name} ({model.id})")
