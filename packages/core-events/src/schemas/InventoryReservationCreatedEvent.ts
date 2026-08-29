import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface InventoryReservationCreatedEventPayload {
  reservationId: string; reservationCode: string; orderId: string; sku: string; quantity: number; expiresAt: Date;
}

export type InventoryReservationCreatedEvent = DomainEvent<InventoryReservationCreatedEventPayload>;

export class InventoryReservationCreatedEventFactory {
  public static create(
    aggregateId: string,
    payload: InventoryReservationCreatedEventPayload,
    producer: string,
    correlationId?: string
  ): InventoryReservationCreatedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'inventory.reservation.created' as EventType,
      aggregateId,
      aggregateType: 'InventoryReservation',
      version: 1,
      timestamp: new Date().toISOString(),
      correlationId: correlationId || crypto.randomUUID(),
      producer,
      payload
    };
  }
}
