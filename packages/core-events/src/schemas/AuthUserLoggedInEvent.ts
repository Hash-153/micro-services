import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface AuthUserLoggedInEventPayload {
  userId: string; email: string; ipAddress?: string; userAgent?: string;
}

export type AuthUserLoggedInEvent = DomainEvent<AuthUserLoggedInEventPayload>;

export class AuthUserLoggedInEventFactory {
  public static create(
    aggregateId: string,
    payload: AuthUserLoggedInEventPayload,
    producer: string,
    correlationId?: string
  ): AuthUserLoggedInEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'auth.user.logged_in' as EventType,
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
