import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface OrderPaidEventPayload {
  orderId: string; paymentTransactionId: string; paidAmountCents: number; currency: string;
}

export type OrderPaidEvent = DomainEvent<OrderPaidEventPayload>;

export class OrderPaidEventFactory {
  public static create(
    aggregateId: string,
    payload: OrderPaidEventPayload,
    producer: string,
    correlationId?: string
  ): OrderPaidEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'order.paid' as EventType,
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
