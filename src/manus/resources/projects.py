"""Projects API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from ..client import Manus
    from ..async_client import AsyncManus


def _is_async_client(client: object) -> bool:
    """Check if client is an async client by checking class name."""
    return type(client).__name__ == "AsyncManus"


class Project(BaseModel):
    """A project resource."""

    model_config = ConfigDict(extra="allow")

    id: str
    object: str = "project"
    name: Optional[str] = None
    description: Optional[str] = None
    instruction: Optional[str] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None


class Projects:
    """Projects API resource."""

    def __init__(self, client: Union[Manus, AsyncManus]) -> None:
        self._client = client

    def create(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        instruction: Optional[str] = None,
        **kwargs: Any,
    ) -> Project:
        """Create a new project.

        Args:
            name: The name of the project.
            description: Optional description of the project.
            instruction: Optional default instruction for tasks in this project.

        Returns:
            The created project.
        """
        params: Dict[str, Any] = {"name": name}
        if description is not None:
            params["description"] = description
        if instruction is not None:
            params["instruction"] = instruction
        params.update(kwargs)

        is_async = _is_async_client(self._client)

        if is_async:
            import asyncio

            return asyncio.get_event_loop().run_until_complete(
                self._client._post(  # type: ignore
                    "/projects",
                    json=params,
                    cast_to=Project,
                )
            )
        else:
            return self._client._post(
                "/projects",
                json=params,
                cast_to=Project,
            )

    def list(
        self,
        *,
        limit: Optional[int] = None,
        **kwargs: Any,
    ) -> List[Project]:
        """List all projects.

        Args:
            limit: Maximum number of projects to return.
            **kwargs: Additional query parameters.

        Returns:
            List of projects.
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        params.update(kwargs)

        is_async = _is_async_client(self._client)

        if is_async:
            import asyncio

            return asyncio.get_event_loop().run_until_complete(
                self._client._get(  # type: ignore
                    "/projects",
                    params=params,
                    cast_to=object,
                )
            ).get("data", [])
        else:
            return self._client._get(
                "/projects",
                params=params,
                cast_to=object,
            ).get("data", [])

    def retrieve(self, project_id: str) -> Project:
        """Retrieve a project by ID.

        Args:
            project_id: The ID of the project.

        Returns:
            The project.
        """
        is_async = _is_async_client(self._client)

        if is_async:
            import asyncio

            return asyncio.get_event_loop().run_until_complete(
                self._client._get(  # type: ignore
                    f"/projects/{project_id}",
                    cast_to=Project,
                )
            )
        else:
            return self._client._get(
                f"/projects/{project_id}",
                cast_to=Project,
            )

    def update(
        self,
        project_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        instruction: Optional[str] = None,
        **kwargs: Any,
    ) -> Project:
        """Update a project.

        Args:
            project_id: The ID of the project.
            name: New name for the project.
            description: New description.
            instruction: New default instruction.

        Returns:
            The updated project.
        """
        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if description is not None:
            params["description"] = description
        if instruction is not None:
            params["instruction"] = instruction
        params.update(kwargs)

        is_async = _is_async_client(self._client)

        if is_async:
            import asyncio

            return asyncio.get_event_loop().run_until_complete(
                self._client._put(  # type: ignore
                    f"/projects/{project_id}",
                    json=params,
                    cast_to=Project,
                )
            )
        else:
            return self._client._put(
                f"/projects/{project_id}",
                json=params,
                cast_to=Project,
            )

    def delete(self, project_id: str) -> bool:
        """Delete a project.

        Args:
            project_id: The ID of the project.

        Returns:
            True if deleted successfully.
        """
        is_async = _is_async_client(self._client)

        if is_async:
            import asyncio

            return asyncio.get_event_loop().run_until_complete(
                self._client._delete(  # type: ignore
                    f"/projects/{project_id}",
                )
            )
        else:
            return self._client._delete(
                f"/projects/{project_id}",
            )
