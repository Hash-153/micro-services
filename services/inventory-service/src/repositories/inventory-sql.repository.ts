import { InventoryStockEntity, InventoryReservationEntity } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export class InventorySqlRepository {
  private logger: Logger;
  private stocks: Map<string, InventoryStockEntity> = new Map(); // key: sku:warehouseId

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async getStock(sku: string, warehouseId: string): Promise<InventoryStockEntity | null> {
    const key = `${sku}:${warehouseId}`;
    return this.stocks.get(key) || null;
  }

  public async setStock(stock: InventoryStockEntity): Promise<InventoryStockEntity> {
    const key = `${stock.sku}:${stock.warehouseId}`;
    this.stocks.set(key, stock);
    this.logger.info(`Stock persisted in SQL repo: SKU ${stock.sku} @ WH ${stock.warehouseId}: onHand=${stock.onHandQuantity}`);
    return stock;
  }
}
