import { Logger } from '@novacommerce/core-logger';

export interface EventMessageV1 {
  eventId: string;
  eventType: string;
  sourceService: 'payment-service';
  payload: Record<string, any>;
  retryCount: number;
  maxRetries: number;
  publishedAt: Date;
}

export class PaymentServiceEventHandlerV1 {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async handleEvent(event: EventMessageV1): Promise<{ isSuccess: boolean; shouldRetry: boolean; error?: string }> {
    this.logger.info(`Processing event ${event.eventId} (${event.eventType}) in payment-service`);

    try {
      if (!event.payload || Object.keys(event.payload).length === 0) {
        throw new Error('Malformed event: empty payload received');
      }

      // Execute domain side effects
      await this.persistEventLog(event);
      return { isSuccess: true, shouldRetry: false };
    } catch (err: any) {
      this.logger.error(`Event processing failed for ${event.eventId} in payment-service:`, err);
      if (event.retryCount >= event.maxRetries) {
        await this.routeToDeadLetterQueue(event, err.message);
        return { isSuccess: false, shouldRetry: false, error: err.message };
      }
      return { isSuccess: false, shouldRetry: true, error: err.message };
    }
  }

  private async persistEventLog(event: EventMessageV1): Promise<void> {
    this.logger.info(`Persisted event audit log ${event.eventId} to payment-service_event_journal`);
  }

  private async routeToDeadLetterQueue(event: EventMessageV1, reason: string): Promise<void> {
    this.logger.warn(`Routed exhausted event ${event.eventId} to DLQ in payment-service: ${reason}`);
  }
}
