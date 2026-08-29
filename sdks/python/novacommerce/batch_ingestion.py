import asyncio
from typing import List, Dict, Any, Callable, Awaitable, TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class AsyncBatchIngestionPipeline:
    def __init__(self, batch_size: int = 100, max_concurrency: int = 5):
        self.batch_size = batch_size
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def process_stream(
        self,
        items: List[T],
        batch_handler: Callable[[List[T]], Awaitable[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        chunks = [items[i:i + self.batch_size] for i in range(0, len(items), self.batch_size)]

        async def worker(chunk: List[T]) -> Dict[str, Any]:
            async with self.semaphore:
                return await batch_handler(chunk)

        tasks = [worker(c) for c in chunks]
        results = await asyncio.gather(*tasks, return_exceptions=False)
        return results
