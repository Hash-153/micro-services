import { InMemoryBaseRepository } from '@novacommerce/core-database';
import { InventoryStockEntity, InventoryReservationEntity } from '@novacommerce/core-types';

export class InMemoryStockRepository extends InMemoryBaseRepository<InventoryStockEntity> {
  public async findBySku(sku: string): Promise<InventoryStockEntity | null> {
    for (const item of this.items.values()) {
      if (item.sku === sku) return JSON.parse(JSON.stringify(item));
    }
    return null;
  }
}

export class InMemoryReservationRepository extends InMemoryBaseRepository<InventoryReservationEntity> {
  public async findByOrderId(orderId: string): Promise<InventoryReservationEntity[]> {
    return Array.from(this.items.values()).filter(r => r.orderId === orderId);
  }
}
