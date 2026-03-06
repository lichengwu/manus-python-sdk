"""Files API resource."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, BinaryIO, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from ..async_client import AsyncManus
    from ..client import Manus


def _is_async_client(client: object) -> bool:
    """Check if client is an async client by checking class name."""
    return type(client).__name__ == "AsyncManus"


class FileObject(BaseModel):
    """A file resource."""

    model_config = ConfigDict(extra="allow")

    id: str
    object: str = "file"
    filename: str
    status: str  # pending, uploaded, deleted
    created_at: Optional[int] = None
    size: Optional[int] = None
    purpose: Optional[str] = None
    upload_url: Optional[str] = None
    upload_expires_at: Optional[str] = None


class Files:
    """Files API resource."""

    def __init__(self, client: Union[Manus, AsyncManus]) -> None:
        self._client = client

    def create(
        self,
        *,
        filename: str,
        purpose: Optional[str] = None,
        **kwargs: Any,
    ) -> FileObject:
        """Create a file record and get presigned upload URL.

        Args:
            filename: Name of the file to upload.
            purpose: Optional purpose of the file (e.g., "assistants", "fine-tune").

        Returns:
            File record with upload URL.

        Note:
            The upload URL expires in 3 minutes. Complete your upload before it expires.
        """
        params: Dict[str, Any] = {"filename": filename}
        if purpose is not None:
            params["purpose"] = purpose
        params.update(kwargs)

        is_async = _is_async_client(self._client)

        if is_async:
            import asyncio

            return asyncio.get_event_loop().run_until_complete(
                self._client._post(  # type: ignore
                    "/files",
                    json=params,
                    cast_to=FileObject,
                )
            )
        else:
            return self._client._post(
                "/files",
                json=params,
                cast_to=FileObject,
            )

    def upload(
        self,
        file_id: str,
        file_content: Union[bytes, BinaryIO, Path, str],
        upload_url: str,
    ) -> bool:
        """Upload file content to the presigned URL.

        Args:
            file_id: The file ID from create().
            file_content: File content as bytes, file path, or file-like object.
            upload_url: The presigned upload URL from create().

        Returns:
            True if upload successful.

        Note:
            This method uses direct HTTP PUT to the presigned URL,
            not through the Manus API client.
        """
        import httpx

        # Read file content
        if isinstance(file_content, (str, Path)):
            with open(file_content, "rb") as f:
                content = f.read()
        elif isinstance(file_content, bytes):
            content = file_content
        else:
            # File-like object
            content = file_content.read()

        # Upload to presigned URL
        response = httpx.put(upload_url, content=content)
        response.raise_for_status()
        return True

    def create_and_upload(
        self,
        *,
        filename: str,
        file_content: Union[bytes, BinaryIO, Path, str],
        purpose: Optional[str] = None,
        **kwargs: Any,
    ) -> FileObject:
        """Create a file record and upload content in one step.

        Args:
            filename: Name of the file.
            file_content: File content.
            purpose: Optional purpose.

        Returns:
            The uploaded file record.
        """
        # Step 1: Create file record
        file_record = self.create(filename=filename, purpose=purpose, **kwargs)

        if not file_record.upload_url:
            raise ValueError("No upload URL returned from file creation")

        # Step 2: Upload content
        self.upload(file_record.id, file_content, file_record.upload_url)

        return file_record

    def list(
        self,
        *,
        limit: Optional[int] = None,
        purpose: Optional[str] = None,
        **kwargs: Any,
    ) -> List[FileObject]:
        """List all files.

        Args:
            limit: Maximum number of files to return.
            purpose: Filter by purpose.

        Returns:
            List of files.
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if purpose is not None:
            params["purpose"] = purpose
        params.update(kwargs)

        is_async = _is_async_client(self._client)

        if is_async:
            import asyncio

            return (
                asyncio.get_event_loop()
                .run_until_complete(
                    self._client._get(  # type: ignore
                        "/files",
                        params=params,
                        cast_to=object,
                    )
                )
                .get("data", [])
            )
        else:
            return self._client._get(
                "/files",
                params=params,
                cast_to=object,
            ).get("data", [])

    def retrieve(self, file_id: str) -> FileObject:
        """Retrieve a file by ID.

        Args:
            file_id: The ID of the file.

        Returns:
            The file.
        """
        is_async = _is_async_client(self._client)

        if is_async:
            import asyncio

            return asyncio.get_event_loop().run_until_complete(
                self._client._get(  # type: ignore
                    f"/files/{file_id}",
                    cast_to=FileObject,
                )
            )
        else:
            return self._client._get(
                f"/files/{file_id}",
                cast_to=FileObject,
            )

    def delete(self, file_id: str) -> bool:
        """Delete a file.

        Args:
            file_id: The ID of the file.

        Returns:
            True if deleted successfully.

        Note:
            Files are automatically deleted after 48 hours.
        """
        is_async = _is_async_client(self._client)

        if is_async:
            import asyncio

            return asyncio.get_event_loop().run_until_complete(
                self._client._delete(  # type: ignore
                    f"/files/{file_id}",
                )
            )
        else:
            return self._client._delete(
                f"/files/{file_id}",
            )
