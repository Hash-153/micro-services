import { IEventBus, EventHandler } from './interfaces.js';
import { DomainEvent, EventType } from '@novacommerce/core-types';
import { ILogger } from '@novacommerce/core-logger';

export class InMemoryEventBus implements IEventBus {
  private readonly handlers: Map<EventType, Set<EventHandler<unknown>>> = new Map();
  private connected: boolean = false;
  private readonly logger?: ILogger;

  constructor(logger?: ILogger) {
    this.logger = logger;
  }

  public async connect(): Promise<void> {
    this.connected = true;
    this.logger?.info('InMemoryEventBus connected.');
  }

  public async disconnect(): Promise<void> {
    this.connected = false;
    this.handlers.clear();
    this.logger?.info('InMemoryEventBus disconnected.');
  }

  public isConnected(): boolean {
    return this.connected;
  }

  public async publish<T>(event: DomainEvent<T>): Promise<boolean> {
    if (!this.connected) {
      throw new Error('EventBus is not connected.');
    }

    const registeredHandlers = this.handlers.get(event.eventType);
    if (!registeredHandlers || registeredHandlers.size === 0) {
      this.logger?.debug(`No handlers registered for event type: ${event.eventType}`);
      return true;
    }

    for (const handler of registeredHandlers) {
      try {
        await handler(event as DomainEvent<unknown>);
      } catch (err) {
        this.logger?.error(`Error handling event ${event.eventType} with handler`, err);
        throw err;
      }
    }

    return true;
  }

  public async publishBatch<T>(events: DomainEvent<T>[]): Promise<boolean[]> {
    const results: boolean[] = [];
    for (const ev of events) {
      const res = await this.publish(ev);
      results.push(res);
    }
    return results;
  }

  public async subscribe<T>(eventType: EventType, handler: EventHandler<T>): Promise<void> {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, new Set());
    }
    this.handlers.get(eventType)!.add(handler as EventHandler<unknown>);
    this.logger?.debug(`Subscribed to event: ${eventType}`);
  }

  public async unsubscribe(eventType: EventType): Promise<void> {
    this.handlers.delete(eventType);
  }
}
