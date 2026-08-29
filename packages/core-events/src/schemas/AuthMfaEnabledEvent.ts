import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface AuthMfaEnabledEventPayload {
  userId: string; email: string; enabledAt: Date;
}

export type AuthMfaEnabledEvent = DomainEvent<AuthMfaEnabledEventPayload>;

export class AuthMfaEnabledEventFactory {
  public static create(
    aggregateId: string,
    payload: AuthMfaEnabledEventPayload,
    producer: string,
    correlationId?: string
  ): AuthMfaEnabledEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'auth.mfa.enabled' as EventType,
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
