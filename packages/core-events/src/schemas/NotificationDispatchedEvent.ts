import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface NotificationDispatchedEventPayload {
  notificationId: string; recipient: string; channel: string; templateId: string; dispatchedAt: Date;
}

export type NotificationDispatchedEvent = DomainEvent<NotificationDispatchedEventPayload>;

export class NotificationDispatchedEventFactory {
  public static create(
    aggregateId: string,
    payload: NotificationDispatchedEventPayload,
    producer: string,
    correlationId?: string
  ): NotificationDispatchedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'notification.sent' as EventType,
      aggregateId,
      aggregateType: 'NotificationLog',
      version: 1,
      timestamp: new Date().toISOString(),
      correlationId: correlationId || crypto.randomUUID(),
      producer,
      payload
    };
  }
}
