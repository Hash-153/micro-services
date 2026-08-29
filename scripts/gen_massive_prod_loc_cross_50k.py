import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_cross_50k():
    print("Generating comprehensive Production Cross-50k Modules...")

    # 1. SDK Python Client Async Pool
    write_file("sdks/python/novacommerce/connection_pool.py", """import asyncio
import httpx
from typing import Optional, Dict, Any

class AsyncConnectionPoolManager:
    def __init__(self, max_connections: int = 100, max_keepalive_connections: int = 20, keepalive_expiry: float = 30.0):
        self.limits = httpx.Limits(
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections,
            keepalive_expiry=keepalive_expiry
        )
        self.timeout = httpx.Timeout(30.0, connect=5.0, read=25.0, write=5.0)

    def create_client(self, base_url: str, default_headers: Optional[Dict[str, str]] = None) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=base_url,
            headers=default_headers or {},
            limits=self.limits,
            timeout=self.timeout,
            http2=True
        )
""")

    # 2. SDK Python Pagination Helpers
    write_file("sdks/python/novacommerce/pagination.py", """from typing import TypeVar, Generic, List, Optional, AsyncIterator, Callable, Awaitable
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
""")

    # 3. TypeScript SDK Client Pagination Helpers
    write_file("sdks/typescript/src/pagination/AsyncPaginator.ts", """import { PaginatedResult } from '@novacommerce/core-types';

export class AsyncPaginator<T> {
  private fetchPageFn: (page: number, limit: number) => Promise<PaginatedResult<T>>;
  private pageSize: number;

  constructor(fetchPageFn: (page: number, limit: number) => Promise<PaginatedResult<T>>, pageSize: number = 50) {
    this.fetchPageFn = fetchPageFn;
    this.pageSize = pageSize;
  }

  public async *[Symbol.asyncIterator](): AsyncIterator<T> {
    let currentPage = 1;
    let hasMore = true;

    while (hasMore) {
      const result = await this.fetchPageFn(currentPage, this.pageSize);
      for (const item of result.items) {
        yield item;
      }

      if (!result.hasNext || currentPage >= result.totalPages) {
        hasMore = false;
      } else {
        currentPage++;
      }
    }
  }

  public async collectAll(): Promise<T[]> {
    const all: T[] = [];
    for await (const item of this) {
      all.push(item);
    }
    return all;
  }
}
""")

    print("Production cross-50k modules generated.")

if __name__ == "__main__":
    generate_prod_cross_50k()
