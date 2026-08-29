import { Logger } from '@novacommerce/core-logger';

export interface CacheEntry<T> {
  value: T;
  expiresAt: number;
}

export class DistributedCacheStore {
  private logger: Logger;
  private store: Map<string, CacheEntry<any>> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async get<T>(key: string): Promise<T | null> {
    const entry = this.store.get(key);
    if (!entry) return null;

    if (Date.now() > entry.expiresAt) {
      this.store.delete(key);
      return null;
    }

    return entry.value as T;
  }

  public async set<T>(key: string, value: T, ttlSeconds: number = 300): Promise<void> {
    const expiresAt = Date.now() + ttlSeconds * 1000;
    this.store.set(key, { value, expiresAt });
  }

  public async delete(key: string): Promise<boolean> {
    return this.store.delete(key);
  }

  public async getOrSet<T>(key: string, fetcher: () => Promise<T>, ttlSeconds: number = 300): Promise<T> {
    const cached = await this.get<T>(key);
    if (cached !== null) return cached;

    const fresh = await fetcher();
    await this.set<T>(key, fresh, ttlSeconds);
    return fresh;
  }
}
