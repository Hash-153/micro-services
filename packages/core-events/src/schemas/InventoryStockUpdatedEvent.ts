import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface InventoryStockUpdatedEventPayload {
  sku: string; warehouseId: string; previousOnHand: number; newOnHand: number;
}

export type InventoryStockUpdatedEvent = DomainEvent<InventoryStockUpdatedEventPayload>;

export class InventoryStockUpdatedEventFactory {
  public static create(
    aggregateId: string,
    payload: InventoryStockUpdatedEventPayload,
    producer: string,
    correlationId?: string
  ): InventoryStockUpdatedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'inventory.stock.updated' as EventType,
      aggregateId,
      aggregateType: 'InventoryStock',
      version: 1,
      timestamp: new Date().toISOString(),
      correlationId: correlationId || crypto.randomUUID(),
      producer,
      payload
    };
  }
}
