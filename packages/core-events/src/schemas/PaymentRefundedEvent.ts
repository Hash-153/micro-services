import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface PaymentRefundedEventPayload {
  refundId: string; originalPaymentId: string; orderId: string; refundAmountCents: number; currency: string; reason: string;
}

export type PaymentRefundedEvent = DomainEvent<PaymentRefundedEventPayload>;

export class PaymentRefundedEventFactory {
  public static create(
    aggregateId: string,
    payload: PaymentRefundedEventPayload,
    producer: string,
    correlationId?: string
  ): PaymentRefundedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'payment.refunded' as EventType,
      aggregateId,
      aggregateType: 'PaymentTransaction',
      version: 1,
      timestamp: new Date().toISOString(),
      correlationId: correlationId || crypto.randomUUID(),
      producer,
      payload
    };
  }
}
