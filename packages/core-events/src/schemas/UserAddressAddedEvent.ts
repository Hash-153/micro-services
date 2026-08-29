import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface UserAddressAddedEventPayload {
  addressId: string; userId: string; countryCode: string; postalCode: string; isDefaultShipping: boolean;
}

export type UserAddressAddedEvent = DomainEvent<UserAddressAddedEventPayload>;

export class UserAddressAddedEventFactory {
  public static create(
    aggregateId: string,
    payload: UserAddressAddedEventPayload,
    producer: string,
    correlationId?: string
  ): UserAddressAddedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'user.address.added' as EventType,
      aggregateId,
      aggregateType: 'Address',
      version: 1,
      timestamp: new Date().toISOString(),
      correlationId: correlationId || crypto.randomUUID(),
      producer,
      payload
    };
  }
}
