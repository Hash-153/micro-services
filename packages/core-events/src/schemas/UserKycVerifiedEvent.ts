import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface UserKycVerifiedEventPayload {
  userId: string; verificationLevel: string; verifiedAt: Date; reviewerId: string;
}

export type UserKycVerifiedEvent = DomainEvent<UserKycVerifiedEventPayload>;

export class UserKycVerifiedEventFactory {
  public static create(
    aggregateId: string,
    payload: UserKycVerifiedEventPayload,
    producer: string,
    correlationId?: string
  ): UserKycVerifiedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'user.kyc.verified' as EventType,
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
