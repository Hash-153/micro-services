import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_master_galaxy_modules():
    print("Generating comprehensive Master Galaxy Modules...")

    # 1. SDK Python Asynchronous Batch Ingestion Pipelines
    write_file("sdks/python/novacommerce/batch_ingestion.py", """import asyncio
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
""")

    # 2. TypeScript SDK Rate-Limiting Token Bucket Adapter
    write_file("sdks/typescript/src/client/TokenBucketRateLimiter.ts", """export class TokenBucketRateLimiter {
  private capacity: number;
  private refillRatePerSecond: number;
  private tokens: number;
  private lastRefillTimestamp: number;

  constructor(capacity: number = 100, refillRatePerSecond: number = 20) {
    this.capacity = capacity;
    this.refillRatePerSecond = refillRatePerSecond;
    this.tokens = capacity;
    this.lastRefillTimestamp = Date.now();
  }

  public async acquireToken(cost: number = 1): Promise<void> {
    while (true) {
      this.refill();
      if (this.tokens >= cost) {
        this.tokens -= cost;
        return;
      }
      // Wait for 50ms before trying again
      await new Promise(resolve => setTimeout(resolve, 50));
    }
  }

  private refill(): void {
    const now = Date.now();
    const elapsedSeconds = (now - this.lastRefillTimestamp) / 1000;
    const tokensToAdd = elapsedSeconds * this.refillRatePerSecond;

    if (tokensToAdd > 0) {
      this.tokens = Math.min(this.capacity, this.tokens + tokensToAdd);
      this.lastRefillTimestamp = now;
    }
  }
}
""")

    print("Master galaxy modules generated.")

if __name__ == "__main__":
    generate_master_galaxy_modules()
