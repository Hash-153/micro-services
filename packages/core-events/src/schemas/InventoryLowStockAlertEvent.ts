import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface InventoryLowStockAlertEventPayload {
  sku: string; warehouseId: string; currentOnHand: number; safetyThreshold: number;
}

export type InventoryLowStockAlertEvent = DomainEvent<InventoryLowStockAlertEventPayload>;

export class InventoryLowStockAlertEventFactory {
  public static create(
    aggregateId: string,
    payload: InventoryLowStockAlertEventPayload,
    producer: string,
    correlationId?: string
  ): InventoryLowStockAlertEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'inventory.stock.low_alert' as EventType,
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
