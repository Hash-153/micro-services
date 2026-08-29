import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface IEventPublisher {
  publish<T>(event: DomainEvent<T>): Promise<boolean>;
  publishBatch<T>(events: DomainEvent<T>[]): Promise<boolean[]>;
}

export type EventHandler<T = unknown> = (event: DomainEvent<T>) => Promise<void>;

export interface IEventSubscriber {
  subscribe<T>(eventType: EventType, handler: EventHandler<T>, queueName?: string): Promise<void>;
  unsubscribe(eventType: EventType): Promise<void>;
}

export interface IEventBus extends IEventPublisher, IEventSubscriber {
  connect(): Promise<void>;
  disconnect(): Promise<void>;
  isConnected(): boolean;
}

export interface OutboxRepository {
  saveOutboxEvent(event: DomainEvent): Promise<void>;
  fetchPendingEvents(limit: number): Promise<DomainEvent[]>;
  markEventPublished(eventId: string): Promise<void>;
  markEventFailed(eventId: string, error: string): Promise<void>;
}
