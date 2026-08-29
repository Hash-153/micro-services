import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface AuthUserRegisteredEventPayload {
  userId: string; email: string; role: string; firstName: string; lastName: string; phoneNumber?: string;
}

export type AuthUserRegisteredEvent = DomainEvent<AuthUserRegisteredEventPayload>;

export class AuthUserRegisteredEventFactory {
  public static create(
    aggregateId: string,
    payload: AuthUserRegisteredEventPayload,
    producer: string,
    correlationId?: string
  ): AuthUserRegisteredEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'auth.user.registered' as EventType,
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
