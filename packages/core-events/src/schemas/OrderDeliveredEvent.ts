import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface OrderDeliveredEventPayload {
  orderId: string; shipmentId: string; deliveredAt: Date; signedBy?: string;
}

export type OrderDeliveredEvent = DomainEvent<OrderDeliveredEventPayload>;

export class OrderDeliveredEventFactory {
  public static create(
    aggregateId: string,
    payload: OrderDeliveredEventPayload,
    producer: string,
    correlationId?: string
  ): OrderDeliveredEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'order.delivered' as EventType,
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
