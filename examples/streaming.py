"""Streaming example for the Manus Python SDK."""

import os

from manus import Manus


def main() -> None:
    # Create a client
    client = Manus(
        api_key=os.environ.get("MANUS_API_KEY"),
    )

    # Create a streaming chat completion
    stream = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a short poem about programming."},
        ],
        model="manus-v1",
        stream=True,
    )

    # Iterate over the streaming response
    print("Streaming response:")
    for chunk in stream:
        # Each chunk contains a delta with the new content
        if chunk.choices and len(chunk.choices) > 0:
            delta = chunk.choices[0].delta
            content = delta.get("content", "")
            if content:
                print(content, end="", flush=True)

    print("\n\nStreaming complete!")


if __name__ == "__main__":
    main()
