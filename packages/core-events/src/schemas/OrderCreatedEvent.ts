import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface OrderCreatedEventPayload {
  orderId: string; orderNumber: string; userId: string; subtotalCents: number; taxCents: number; totalCents: number; currency: string; itemsCount: number;
}

export type OrderCreatedEvent = DomainEvent<OrderCreatedEventPayload>;

export class OrderCreatedEventFactory {
  public static create(
    aggregateId: string,
    payload: OrderCreatedEventPayload,
    producer: string,
    correlationId?: string
  ): OrderCreatedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'order.created' as EventType,
      aggregateId,
      aggregateType: 'Order',
      version: 1,
      timestamp: new Date().toISOString(),
      correlationId: correlationId || crypto.randomUUID(),
      producer,
      payload
    };
  }
}
