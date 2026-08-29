import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface UserProfileUpdatedEventPayload {
  userId: string; firstName: string; lastName: string; timeZone: string; locale: string;
}

export type UserProfileUpdatedEvent = DomainEvent<UserProfileUpdatedEventPayload>;

export class UserProfileUpdatedEventFactory {
  public static create(
    aggregateId: string,
    payload: UserProfileUpdatedEventPayload,
    producer: string,
    correlationId?: string
  ): UserProfileUpdatedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'user.profile.updated' as EventType,
      aggregateId,
      aggregateType: 'UserProfile',
      version: 1,
      timestamp: new Date().toISOString(),
      correlationId: correlationId || crypto.randomUUID(),
      producer,
      payload
    };
  }
}
