import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface PaymentAuthorizedEventPayload {
  paymentId: string; orderId: string; amountCents: number; currency: string; provider: string; transactionReference: string;
}

export type PaymentAuthorizedEvent = DomainEvent<PaymentAuthorizedEventPayload>;

export class PaymentAuthorizedEventFactory {
  public static create(
    aggregateId: string,
    payload: PaymentAuthorizedEventPayload,
    producer: string,
    correlationId?: string
  ): PaymentAuthorizedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'payment.authorized' as EventType,
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
