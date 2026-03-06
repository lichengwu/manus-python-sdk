"""Pagination support for the Manus Python SDK."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    TypeVar,
)

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class PageInfo(BaseModel):
    """Pagination information for a list response."""

    model_config = ConfigDict(extra="allow")

    has_more: bool = False
    before: Optional[str] = None
    after: Optional[str] = None


class CursorPage(BaseModel, Generic[T]):
    """A page of cursor-paginated results."""

    model_config = ConfigDict(extra="allow")

    object: str = "list"
    data: List[T]
    has_more: bool = False
    first_id: Optional[str] = None
    last_id: Optional[str] = None
    url: Optional[str] = None

    def __getitem__(self, index: int) -> T:
        return self.data[index]

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator[T]:
        return iter(self.data)


class AsyncCursorPage(CursorPage[T], Generic[T]):
    """An async page of cursor-paginated results."""

    pass


class CursorPaginator(Generic[T]):
    """Paginator for cursor-based pagination."""

    def __init__(
        self,
        *,
        client: Any,
        page: CursorPage[T],
        options: Dict[str, Any],
        model: type[T],
    ) -> None:
        self._client = client
        self._page = page
        self._options = options
        self._model = model
        self._cursor: Optional[str] = page.last_id

    def get_page(self, *, after: Optional[str] = None) -> Dict[str, Any]:
        """Get the parameters for the next page."""
        params = dict(self._options)
        if after is not None:
            params["after"] = after
        elif self._cursor is not None:
            params["after"] = self._cursor
        return params

    def __iter__(self) -> Iterator[CursorPage[T]]:
        """Iterate over pages."""
        page = self._page
        while True:
            yield page
            if not page.has_more:
                break
            # Get next page
            self.get_page()
            # Call the API to get the next page
            # This would be implemented by the calling class
            raise NotImplementedError("Subclasses must implement __iter__")

    def auto_pager(self) -> Iterator[T]:
        """Iterate over all items in all pages."""
        for page in self:
            for item in page.data:
                yield item


class AsyncCursorPaginator(CursorPaginator[T], Generic[T]):
    """Async paginator for cursor-based pagination."""

    async def __aiter__(self) -> AsyncIterator[CursorPage[T]]:
        """Iterate over pages asynchronously."""
        page = self._page
        while True:
            yield page
            if not page.has_more:
                break
            # Get next page
            self.get_page()
            # Call the API to get the next page
            # This would be implemented by the calling class
            raise NotImplementedError("Subclasses must implement __aiter__")

    async def auto_pager(self) -> AsyncIterator[T]:
        """Iterate over all items in all pages asynchronously."""
        async for page in self:
            for item in page.data:
                yield item
