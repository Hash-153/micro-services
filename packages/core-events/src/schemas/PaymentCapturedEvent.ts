import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface PaymentCapturedEventPayload {
  paymentId: string; orderId: string; amountCents: number; currency: string; providerTransactionId: string;
}

export type PaymentCapturedEvent = DomainEvent<PaymentCapturedEventPayload>;

export class PaymentCapturedEventFactory {
  public static create(
    aggregateId: string,
    payload: PaymentCapturedEventPayload,
    producer: string,
    correlationId?: string
  ): PaymentCapturedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'payment.captured' as EventType,
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
