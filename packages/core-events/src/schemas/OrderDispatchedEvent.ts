import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface OrderDispatchedEventPayload {
  orderId: string; shipmentId: string; carrier: string; trackingNumber: string;
}

export type OrderDispatchedEvent = DomainEvent<OrderDispatchedEventPayload>;

export class OrderDispatchedEventFactory {
  public static create(
    aggregateId: string,
    payload: OrderDispatchedEventPayload,
    producer: string,
    correlationId?: string
  ): OrderDispatchedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'order.dispatched' as EventType,
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
