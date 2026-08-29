import { Logger } from '@novacommerce/core-logger';

export class ApiGatewayCacheStoreV4 {
  private memoryCache: Map<string, { value: any; expiresAt: number }> = new Map();
  private logger: Logger;
  private defaultTtlMs: number;

  constructor(logger: Logger, defaultTtlMs: number = 300000) { // 5 mins
    this.logger = logger;
    this.defaultTtlMs = defaultTtlMs;
  }

  public async get<T>(key: string): Promise<T | null> {
    const entry = this.memoryCache.get(key);
    if (!entry) return null;

    if (Date.now() > entry.expiresAt) {
      this.memoryCache.delete(key);
      this.logger.info(`Cache expired for key [${key}] in api-gateway`);
      return null;
    }

    return entry.value as T;
  }

  public async set<T>(key: string, value: T, ttlMs?: number): Promise<void> {
    const expiresAt = Date.now() + (ttlMs || this.defaultTtlMs);
    this.memoryCache.set(key, { value, expiresAt });
  }

  public async del(key: string): Promise<boolean> {
    return this.memoryCache.delete(key);
  }

  public async clearPrefix(prefix: string): Promise<number> {
    let count = 0;
    for (const k of this.memoryCache.keys()) {
      if (k.startsWith(prefix)) {
        this.memoryCache.delete(k);
        count++;
      }
    }
    return count;
  }
}
