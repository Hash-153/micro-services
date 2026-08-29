import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface OrderPaymentPendingEventPayload {
  orderId: string; orderNumber: string; totalCents: number; currency: string;
}

export type OrderPaymentPendingEvent = DomainEvent<OrderPaymentPendingEventPayload>;

export class OrderPaymentPendingEventFactory {
  public static create(
    aggregateId: string,
    payload: OrderPaymentPendingEventPayload,
    producer: string,
    correlationId?: string
  ): OrderPaymentPendingEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'order.payment_pending' as EventType,
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
