import { PaginatedResult } from '@novacommerce/core-types';

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
