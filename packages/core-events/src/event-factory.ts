import { DomainEvent, EventType } from '@novacommerce/core-types';
import { randomUUID } from 'crypto';

export class DomainEventFactory {
  public static create<T>(
    eventType: EventType,
    aggregateId: string,
    aggregateType: string,
    payload: T,
    producer: string,
    correlationId: string = randomUUID(),
    causationId?: string,
    version: number = 1
  ): DomainEvent<T> {
    return {
      id: randomUUID(),
      eventType,
      aggregateId,
      aggregateType,
      version,
      timestamp: new Date().toISOString(),
      correlationId,
      causationId,
      producer,
      payload
    };
  }
}
