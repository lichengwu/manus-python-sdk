"""Models API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Union

from pydantic import BaseModel, ConfigDict

from ..pagination import AsyncCursorPage, CursorPage

if TYPE_CHECKING:
    from ..async_client import AsyncManus
    from ..client import Manus


def _is_async_client(client: object) -> bool:
    """Check if client is an async client by checking class name."""
    return type(client).__name__ == "AsyncManus"


class Model(BaseModel):
    """A model resource."""

    model_config = ConfigDict(extra="allow")

    id: str
    object: str = "model"
    created: Optional[int] = None
    owned_by: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    context_window: Optional[int] = None
    input_modalities: Optional[List[str]] = None
    output_modalities: Optional[List[str]] = None


class Models:
    """Models API resource."""

    def __init__(self, client: Union[Manus, AsyncManus]) -> None:
        self._client = client

    def list(
        self,
        *,
        limit: Optional[int] = None,
        after: Optional[str] = None,
        **kwargs: Any,
    ) -> CursorPage[Model]:
        """List available models."""

        params = {}
        if limit is not None:
            params["limit"] = limit
        if after is not None:
            params["after"] = after
        params.update(kwargs)

        is_async = _is_async_client(self._client)

        if is_async:
            import asyncio

            return asyncio.get_event_loop().run_until_complete(
                self._client._get(  # type: ignore
                    "/models",
                    params=params,
                    cast_to=CursorPage[Model],
                )
            )
        else:
            return self._client._get(
                "/models",
                params=params,
                cast_to=CursorPage[Model],
            )

    async def list_async(
        self,
        *,
        limit: Optional[int] = None,
        after: Optional[str] = None,
        **kwargs: Any,
    ) -> AsyncCursorPage[Model]:
        """List available models asynchronously."""
        params = {}
        if limit is not None:
            params["limit"] = limit
        if after is not None:
            params["after"] = after
        params.update(kwargs)

        return await self._client._get(
            "/models",
            params=params,
            cast_to=AsyncCursorPage[Model],
        )

    def retrieve(self, model_id: str) -> Model:
        """Retrieve a model by ID."""

        is_async = _is_async_client(self._client)

        if is_async:
            import asyncio

            return asyncio.get_event_loop().run_until_complete(
                self._client._get(  # type: ignore
                    f"/models/{model_id}",
                    cast_to=Model,
                )
            )
        else:
            return self._client._get(
                f"/models/{model_id}",
                cast_to=Model,
            )

    async def retrieve_async(self, model_id: str) -> Model:
        """Retrieve a model by ID asynchronously."""
        return await self._client._get(
            f"/models/{model_id}",
            cast_to=Model,
        )

    def delete(self, model_id: str) -> bool:
        """Delete a model by ID."""

        is_async = _is_async_client(self._client)

        if is_async:
            import asyncio

            return asyncio.get_event_loop().run_until_complete(
                self._client._delete(  # type: ignore
                    f"/models/{model_id}",
                )
            )
        else:
            return self._client._delete(
                f"/models/{model_id}",
            )

    async def delete_async(self, model_id: str) -> bool:
        """Delete a model by ID asynchronously."""
        return await self._client._delete(
            f"/models/{model_id}",
        )
