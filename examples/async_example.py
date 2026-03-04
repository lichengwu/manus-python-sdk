"""Asynchronous usage example for the Manus Python SDK."""

import asyncio
import os

from manus import AsyncManus


async def main() -> None:
    # Create an async client
    # The API key is read from the MANUS_API_KEY environment variable by default
    async with AsyncManus(
        api_key=os.environ.get("MANUS_API_KEY"),
        # base_url="https://api.manus.ai/v1",  # Optional: custom base URL
        # timeout=600,  # Optional: request timeout in seconds
    ) as client:
        # Create a chat completion asynchronously
        response = await client.chat.completions.create_async(
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

        # List available models asynchronously
        models = await client.models.list_async()
        print(f"\nAvailable models: {[m.id for m in models.data]}")

        # Retrieve a specific model asynchronously
        model = await client.models.retrieve_async("manus-v1")
        print(f"\nModel details: {model.name} ({model.id})")


if __name__ == "__main__":
    asyncio.run(main())
