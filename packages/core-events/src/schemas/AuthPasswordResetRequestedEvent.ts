import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface AuthPasswordResetRequestedEventPayload {
  userId: string; email: string; resetToken: string; expiresAt: Date;
}

export type AuthPasswordResetRequestedEvent = DomainEvent<AuthPasswordResetRequestedEventPayload>;

export class AuthPasswordResetRequestedEventFactory {
  public static create(
    aggregateId: string,
    payload: AuthPasswordResetRequestedEventPayload,
    producer: string,
    correlationId?: string
  ): AuthPasswordResetRequestedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'auth.password.reset_requested' as EventType,
      aggregateId,
      aggregateType: 'User',
      version: 1,
      timestamp: new Date().toISOString(),
      correlationId: correlationId || crypto.randomUUID(),
      producer,
      payload
    };
  }
}
