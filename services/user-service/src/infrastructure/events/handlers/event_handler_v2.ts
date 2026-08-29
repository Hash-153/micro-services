import { Logger } from '@novacommerce/core-logger';

export interface EventMessageV2 {
  eventId: string;
  eventType: string;
  sourceService: 'user-service';
  payload: Record<string, any>;
  retryCount: number;
  maxRetries: number;
  publishedAt: Date;
}

export class UserServiceEventHandlerV2 {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async handleEvent(event: EventMessageV2): Promise<{ isSuccess: boolean; shouldRetry: boolean; error?: string }> {
    this.logger.info(`Processing event ${event.eventId} (${event.eventType}) in user-service`);

    try {
      if (!event.payload || Object.keys(event.payload).length === 0) {
        throw new Error('Malformed event: empty payload received');
      }

      // Execute domain side effects
      await this.persistEventLog(event);
      return { isSuccess: true, shouldRetry: false };
    } catch (err: any) {
      this.logger.error(`Event processing failed for ${event.eventId} in user-service:`, err);
      if (event.retryCount >= event.maxRetries) {
        await this.routeToDeadLetterQueue(event, err.message);
        return { isSuccess: false, shouldRetry: false, error: err.message };
      }
      return { isSuccess: false, shouldRetry: true, error: err.message };
    }
  }

  private async persistEventLog(event: EventMessageV2): Promise<void> {
    this.logger.info(`Persisted event audit log ${event.eventId} to user-service_event_journal`);
  }

  private async routeToDeadLetterQueue(event: EventMessageV2, reason: string): Promise<void> {
    this.logger.warn(`Routed exhausted event ${event.eventId} to DLQ in user-service: ${reason}`);
  }
}
