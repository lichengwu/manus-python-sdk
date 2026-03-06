"""Webhooks API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from ..async_client import AsyncManus
    from ..client import Manus


def _is_async_client(client: object) -> bool:
    """Check if client is an async client by checking class name."""
    return type(client).__name__ == "AsyncManus"


class Webhook(BaseModel):
    """A webhook resource."""

    model_config = ConfigDict(extra="allow")

    id: str
    object: str = "webhook"
    url: str
    events: Optional[List[str]] = None
    created_at: Optional[int] = None
    active: Optional[bool] = None


class Webhooks:
    """Webhooks API resource."""

    def __init__(self, client: Union[Manus, AsyncManus]) -> None:
        self._client = client

    def create(
        self,
        *,
        url: str,
        events: Optional[List[str]] = None,
        active: Optional[bool] = None,
        **kwargs: Any,
    ) -> Webhook:
        """Create a new webhook.

        Args:
            url: The URL to send webhook events to.
            events: List of event types to subscribe to.
                Common events: task.created, task.completed, task.failed, task.updated
            active: Whether the webhook is active (default: True).

        Returns:
            The created webhook.
        """
        params: Dict[str, Any] = {"url": url}
        if events is not None:
            params["events"] = events
        if active is not None:
            params["active"] = active
        params.update(kwargs)

        is_async = _is_async_client(self._client)

        if is_async:
            import asyncio

            return asyncio.get_event_loop().run_until_complete(
                self._client._post(  # type: ignore
                    "/webhooks",
                    json=params,
                    cast_to=Webhook,
                )
            )
        else:
            return self._client._post(
                "/webhooks",
                json=params,
                cast_to=Webhook,
            )

    def list(
        self,
        *,
        limit: Optional[int] = None,
        **kwargs: Any,
    ) -> List[Webhook]:
        """List all webhooks.

        Args:
            limit: Maximum number of webhooks to return.

        Returns:
            List of webhooks.
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        params.update(kwargs)

        is_async = _is_async_client(self._client)

        if is_async:
            import asyncio

            return (
                asyncio.get_event_loop()
                .run_until_complete(
                    self._client._get(  # type: ignore
                        "/webhooks",
                        params=params,
                        cast_to=object,
                    )
                )
                .get("data", [])
            )
        else:
            return self._client._get(
                "/webhooks",
                params=params,
                cast_to=object,
            ).get("data", [])

    def retrieve(self, webhook_id: str) -> Webhook:
        """Retrieve a webhook by ID.

        Args:
            webhook_id: The ID of the webhook.

        Returns:
            The webhook.
        """
        is_async = _is_async_client(self._client)

        if is_async:
            import asyncio

            return asyncio.get_event_loop().run_until_complete(
                self._client._get(  # type: ignore
                    f"/webhooks/{webhook_id}",
                    cast_to=Webhook,
                )
            )
        else:
            return self._client._get(
                f"/webhooks/{webhook_id}",
                cast_to=Webhook,
            )

    def delete(self, webhook_id: str) -> bool:
        """Delete a webhook.

        Args:
            webhook_id: The ID of the webhook.

        Returns:
            True if deleted successfully.
        """
        is_async = _is_async_client(self._client)

        if is_async:
            import asyncio

            return asyncio.get_event_loop().run_until_complete(
                self._client._delete(  # type: ignore
                    f"/webhooks/{webhook_id}",
                )
            )
        else:
            return self._client._delete(
                f"/webhooks/{webhook_id}",
            )

    @staticmethod
    def verify_signature(
        payload: str,
        signature: str,
        secret: str,
    ) -> bool:
        """Verify a webhook signature.

        Args:
            payload: The raw webhook payload (JSON string).
            signature: The signature from the webhook header.
            secret: Your webhook signing secret.

        Returns:
            True if signature is valid.

        Note:
            Always verify webhook signatures to ensure the request
            is from Manus and not a malicious actor.
        """
        import hashlib
        import hmac

        # Compute expected signature
        expected_signature = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256,
        ).hexdigest()

        # Compare signatures securely
        return hmac.compare_digest(
            f"sha256={expected_signature}",
            signature,
        )
