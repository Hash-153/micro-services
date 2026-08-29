import { CommodityCodeMapping } from './commodity-code-classifier.js';

export class TariffCacheManager {
  private cache: Map<string, CommodityCodeMapping> = new Map();
  private ttlMs: number;
  private lastFetched: number = 0;

  constructor(ttlMs: number = 3600000) { // 1 hour default TTL
    this.ttlMs = ttlMs;
  }

  public get(categorySlug: string): CommodityCodeMapping | undefined {
    if (Date.now() - this.lastFetched > this.ttlMs) {
      this.cache.clear();
      return undefined;
    }
    return this.cache.get(categorySlug);
  }

  public set(categorySlug: string, mapping: CommodityCodeMapping): void {
    this.cache.set(categorySlug, mapping);
    this.lastFetched = Date.now();
  }
}
