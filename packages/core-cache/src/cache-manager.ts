export interface CacheEntry<T> {
  key: string;
  value: T;
  expiresAt: number;
  createdAt: number;
  accessCount: number;
  lastAccessedAt: number;
}

export interface CacheConfig {
  ttlSeconds: number;
  maxSize: number;
  evictionPolicy: 'LRU' | 'LFU' | 'FIFO';
}

export class CacheManager<T = any> {
  private cache: Map<string, CacheEntry<T>> = new Map();
  private config: CacheConfig;

  constructor(config: CacheConfig) {
    this.config = {
      ttlSeconds: config.ttlSeconds || 300,
      maxSize: config.maxSize || 1000,
      evictionPolicy: config.evictionPolicy || 'LRU'
    };
  }

  public async get(key: string): Promise<T | null> {
    const entry = this.cache.get(key);
    
    if (!entry) {
      return null;
    }

    // Check if expired
    if (Date.now() > entry.expiresAt) {
      this.cache.delete(key);
      return null;
    }

    // Update access statistics
    entry.accessCount++;
    entry.lastAccessedAt = Date.now();
    this.cache.set(key, entry);

    return entry.value;
  }

  public async set(key: string, value: T, ttlSeconds?: number): Promise<void> {
    const ttl = ttlSeconds || this.config.ttlSeconds;
    const entry: CacheEntry<T> = {
      key,
      value,
      expiresAt: Date.now() + (ttl * 1000),
      createdAt: Date.now(),
      accessCount: 0,
      lastAccessedAt: Date.now()
    };

    // Check if we need to evict entries
    if (this.cache.size >= this.config.maxSize) {
      this.evict();
    }

    this.cache.set(key, entry);
  }

  public async delete(key: string): Promise<boolean> {
    return this.cache.delete(key);
  }

  public async clear(): Promise<void> {
    this.cache.clear();
  }

  public async has(key: string): Promise<boolean> {
    const entry = this.cache.get(key);
    if (!entry) {
      return false;
    }

    // Check if expired
    if (Date.now() > entry.expiresAt) {
      this.cache.delete(key);
      return false;
    }

    return true;
  }

  public async size(): Promise<number> {
    // Clean expired entries first
    this.cleanExpired();
    return this.cache.size;
  }

  public async getStats(): Promise<{
    size: number;
    hitRate: number;
    totalAccesses: number;
    oldestEntry: number;
  }> {
    let totalAccesses = 0;
    let oldestEntry = Date.now();

    for (const entry of this.cache.values()) {
      totalAccesses += entry.accessCount;
      if (entry.createdAt < oldestEntry) {
        oldestEntry = entry.createdAt;
      }
    }

    const hitRate = totalAccesses > 0 ? totalAccesses / (totalAccesses + this.cache.size) : 0;

    return {
      size: this.cache.size,
      hitRate,
      totalAccesses,
      oldestEntry
    };
  }

  private evict(): void {
    switch (this.config.evictionPolicy) {
      case 'LRU':
        this.evictLRU();
        break;
      case 'LFU':
        this.evictLFU();
        break;
      case 'FIFO':
        this.evictFIFO();
        break;
    }
  }

  private evictLRU(): void {
    let lruKey: string | null = null;
    let oldestAccess = Date.now();

    for (const [key, entry] of this.cache.entries()) {
      if (entry.lastAccessedAt < oldestAccess) {
        oldestAccess = entry.lastAccessedAt;
        lruKey = key;
      }
    }

    if (lruKey) {
      this.cache.delete(lruKey);
    }
  }

  private evictLFU(): void {
    let lfuKey: string | null = null;
    let lowestAccess = Infinity;

    for (const [key, entry] of this.cache.entries()) {
      if (entry.accessCount < lowestAccess) {
        lowestAccess = entry.accessCount;
        lfuKey = key;
      }
    }

    if (lfuKey) {
      this.cache.delete(lfuKey);
    }
  }

  private evictFIFO(): void {
    let fifoKey: string | null = null;
    let oldestCreation = Date.now();

    for (const [key, entry] of this.cache.entries()) {
      if (entry.createdAt < oldestCreation) {
        oldestCreation = entry.createdAt;
        fifoKey = key;
      }
    }

    if (fifoKey) {
      this.cache.delete(fifoKey);
    }
  }

  private cleanExpired(): void {
    const now = Date.now();
    for (const [key, entry] of this.cache.entries()) {
      if (now > entry.expiresAt) {
        this.cache.delete(key);
      }
    }
  }
}
