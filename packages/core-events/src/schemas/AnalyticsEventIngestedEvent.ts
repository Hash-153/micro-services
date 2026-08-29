import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface AnalyticsEventIngestedEventPayload {
  eventId: string; eventName: string; userId?: string; sessionId?: string; timestamp: Date;
}

export type AnalyticsEventIngestedEvent = DomainEvent<AnalyticsEventIngestedEventPayload>;

export class AnalyticsEventIngestedEventFactory {
  public static create(
    aggregateId: string,
    payload: AnalyticsEventIngestedEventPayload,
    producer: string,
    correlationId?: string
  ): AnalyticsEventIngestedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'analytics.event.ingested' as EventType,
      aggregateId,
      aggregateType: 'AnalyticsEvent',
      version: 1,
      timestamp: new Date().toISOString(),
      correlationId: correlationId || crypto.randomUUID(),
      producer,
      payload
    };
  }
}
