#!/usr/bin/env python3
"""
Webhook Example

Demonstrates how to manage webhooks with Manus API.
"""

import os
from manus import Manus, Webhooks

# Initialize client
client = Manus(api_key=os.environ.get("MANUS_API_KEY", "your-api-key"))


def create_webhook_example():
    """Example: Create a new webhook."""
    
    print("Creating webhook...")
    
    webhook = client.webhooks.create(
        url="https://your-server.com/webhook",
        events=[
            "task.created",
            "task.completed",
            "task.failed",
            "task.updated",
        ],
        active=True,
    )
    
    print(f"Webhook created: {webhook.id}")
    print(f"URL: {webhook.url}")
    print(f"Events: {webhook.events}")
    
    return webhook.id


def list_webhooks_example():
    """Example: List all webhooks."""
    
    print("\nListing webhooks...")
    
    webhooks = client.webhooks.list()
    
    for webhook in webhooks:
        print(f"  - {webhook.id}: {webhook.url} (active: {webhook.active})")


def delete_webhook_example(webhook_id: str):
    """Example: Delete a webhook."""
    
    print(f"\nDeleting webhook: {webhook_id}")
    
    result = client.webhooks.delete(webhook_id)
    
    print(f"Deleted: {result}")


def verify_webhook_signature_example():
    """Example: Verify webhook signature."""
    
    print("\nVerifying webhook signature...")
    
    # Example payload and signature (replace with actual values from request)
    payload = '{"event": "task.completed", "data": {"id": "task123"}}'
    signature = "sha256=abc123..."  # From X-Manus-Signature header
    secret = "your-webhook-secret"  # Store securely
    
    is_valid = Webhooks.verify_signature(
        payload=payload,
        signature=signature,
        secret=secret,
    )
    
    if is_valid:
        print("✓ Signature is valid!")
    else:
        print("✗ Signature is INVALID!")
    
    return is_valid


def flask_webhook_handler_example():
    """
    Example: Flask webhook handler.
    
    Add this to your Flask app to handle Manus webhooks.
    """
    from flask import Flask, request, abort
    
    app = Flask(__name__)
    WEBHOOK_SECRET = os.environ.get("MANUS_WEBHOOK_SECRET", "your-secret")
    
    @app.route("/webhook", methods=["POST"])
    def handle_webhook():
        # Get raw payload and signature
        payload = request.get_data(as_text=True)
        signature = request.headers.get("X-Manus-Signature", "")
        
        # Verify signature
        if not Webhooks.verify_signature(payload, signature, WEBHOOK_SECRET):
            abort(401, description="Invalid signature")
        
        # Parse and handle event
        import json
        event = json.loads(payload)
        event_type = event.get("event")
        event_data = event.get("data")
        
        print(f"Received event: {event_type}")
        
        if event_type == "task.completed":
            print(f"Task completed: {event_data.get('id')}")
            # Handle completed task
        elif event_type == "task.failed":
            print(f"Task failed: {event_data.get('id')}")
            # Handle failed task
        elif event_type == "task.created":
            print(f"Task created: {event_data.get('id')}")
            # Handle new task
        
        return {"status": "ok"}, 200
    
    return app


if __name__ == "__main__":
    # Run examples
    webhook_id = create_webhook_example()
    # list_webhooks_example()
    # verify_webhook_signature_example()
    # delete_webhook_example(webhook_id)
    
    print("\n✓ Webhook example completed!")
