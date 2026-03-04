"""Chat completion example for the Manus Python SDK."""

import os

from manus import Manus


def main() -> None:
    # Create a client
    client = Manus(
        api_key=os.environ.get("MANUS_API_KEY"),
    )

    # Basic chat completion
    print("=== Basic Chat Completion ===")
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"},
        ],
        model="manus-v1",
    )
    print(f"Response: {response.choices[0].message.content}")

    # Chat completion with temperature and max_tokens
    print("\n=== Chat Completion with Options ===")
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a creative writer."},
            {"role": "user", "content": "Write a haiku about coding."},
        ],
        model="manus-v1",
        temperature=0.8,
        max_tokens=100,
        top_p=0.95,
    )
    print(f"Response: {response.choices[0].message.content}")
    print(f"Usage: {response.usage}")

    # Chat completion with conversation history
    print("\n=== Chat Completion with History ===")
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "I'm learning Python."},
        {"role": "assistant", "content": "That's great! Python is a wonderful language."},
        {"role": "user", "content": "What should I learn next?"},
    ]
    response = client.chat.completions.create(
        messages=messages,
        model="manus-v1",
    )
    print(f"Response: {response.choices[0].message.content}")


if __name__ == "__main__":
    main()
