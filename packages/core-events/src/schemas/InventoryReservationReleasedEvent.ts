import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface InventoryReservationReleasedEventPayload {
  reservationId: string; orderId: string; sku: string; quantity: number;
}

export type InventoryReservationReleasedEvent = DomainEvent<InventoryReservationReleasedEventPayload>;

export class InventoryReservationReleasedEventFactory {
  public static create(
    aggregateId: string,
    payload: InventoryReservationReleasedEventPayload,
    producer: string,
    correlationId?: string
  ): InventoryReservationReleasedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'inventory.reservation.released' as EventType,
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
