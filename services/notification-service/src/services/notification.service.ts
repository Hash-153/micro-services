import { ILogger } from '@novacommerce/core-logger';
import { randomUUID } from 'crypto';

export interface NotificationPayload {
  recipient: string;
  channel: 'EMAIL' | 'SMS' | 'PUSH' | 'WEBHOOK';
  template: string;
  data: Record<string, unknown>;
}

export class NotificationService {
  private readonly logger: ILogger;
  private readonly dispatched: Array<NotificationPayload & { id: string; timestamp: Date }> = [];

  constructor(logger: ILogger) {
    this.logger = logger.child({ component: 'NotificationService' });
  }

  public async send(payload: NotificationPayload): Promise<{ id: string; status: string }> {
    const id = randomUUID();
    this.logger.info(`Dispatching ${payload.channel} notification to ${payload.recipient} [Template: ${payload.template}]`);
    
    this.dispatched.push({
      ...payload,
      id,
      timestamp: new Date()
    });

    return { id, status: 'DELIVERED' };
  }

  public getDispatchedCount(): number {
    return this.dispatched.length;
  }
}
