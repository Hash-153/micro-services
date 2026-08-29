from typing import TypeVar, Generic, List, Optional, AsyncIterator, Callable, Awaitable
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class PageResult(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_previous: bool

class AsyncPaginator(Generic[T]):
    def __init__(self, fetch_page_fn: Callable[[int, int], Awaitable[PageResult[T]]], page_size: int = 50):
        self.fetch_page_fn = fetch_page_fn
        self.page_size = page_size

    async def __aiter__(self) -> AsyncIterator[T]:
        current_page = 1
        has_more = True

        while has_more:
            result = await self.fetch_page_fn(current_page, self.page_size)
            for item in result.items:
                yield item

            if not result.has_next or current_page >= result.total_pages:
                has_more = False
            else:
                current_page += 1
