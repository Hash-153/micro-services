import { Logger } from '@novacommerce/core-logger';

export interface SkuInventorySnapshot {
  sku: string;
  totalOnHand: number;
  totalReserved: number;
  totalAvailable: number;
  isInStock: boolean;
  lastSyncedAt: Date;
}

export class InventorySyncService {
  private logger: Logger;
  private stockCache: Map<string, SkuInventorySnapshot> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public handleStockUpdatedEvent(payload: { sku: string; onHand: number; reserved: number }): void {
    const available = Math.max(0, payload.onHand - payload.reserved);
    const snapshot: SkuInventorySnapshot = {
      sku: payload.sku,
      totalOnHand: payload.onHand,
      totalReserved: payload.reserved,
      totalAvailable: available,
      isInStock: available > 0,
      lastSyncedAt: new Date()
    };

    this.stockCache.set(payload.sku, snapshot);
    this.logger.info(`Catalog stock cache updated for SKU ${payload.sku}: available=${available}`);
  }

  public getCachedStock(sku: string): SkuInventorySnapshot | undefined {
    return this.stockCache.get(sku);
  }
}
