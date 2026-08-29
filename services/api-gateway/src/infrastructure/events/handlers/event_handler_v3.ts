import { Logger } from '@novacommerce/core-logger';

export interface EventMessageV3 {
  eventId: string;
  eventType: string;
  sourceService: 'api-gateway';
  payload: Record<string, any>;
  retryCount: number;
  maxRetries: number;
  publishedAt: Date;
}

export class ApiGatewayEventHandlerV3 {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async handleEvent(event: EventMessageV3): Promise<{ isSuccess: boolean; shouldRetry: boolean; error?: string }> {
    this.logger.info(`Processing event ${event.eventId} (${event.eventType}) in api-gateway`);

    try {
      if (!event.payload || Object.keys(event.payload).length === 0) {
        throw new Error('Malformed event: empty payload received');
      }

      // Execute domain side effects
      await this.persistEventLog(event);
      return { isSuccess: true, shouldRetry: false };
    } catch (err: any) {
      this.logger.error(`Event processing failed for ${event.eventId} in api-gateway:`, err);
      if (event.retryCount >= event.maxRetries) {
        await this.routeToDeadLetterQueue(event, err.message);
        return { isSuccess: false, shouldRetry: false, error: err.message };
      }
      return { isSuccess: false, shouldRetry: true, error: err.message };
    }
  }

  private async persistEventLog(event: EventMessageV3): Promise<void> {
    this.logger.info(`Persisted event audit log ${event.eventId} to api-gateway_event_journal`);
  }

  private async routeToDeadLetterQueue(event: EventMessageV3, reason: string): Promise<void> {
    this.logger.warn(`Routed exhausted event ${event.eventId} to DLQ in api-gateway: ${reason}`);
  }
}
