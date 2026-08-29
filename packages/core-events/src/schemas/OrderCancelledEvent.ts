import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface OrderCancelledEventPayload {
  orderId: string; reason: string; cancelledBy: string; compensationTriggered: boolean;
}

export type OrderCancelledEvent = DomainEvent<OrderCancelledEventPayload>;

export class OrderCancelledEventFactory {
  public static create(
    aggregateId: string,
    payload: OrderCancelledEventPayload,
    producer: string,
    correlationId?: string
  ): OrderCancelledEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'order.cancelled' as EventType,
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
