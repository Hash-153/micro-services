import { ILogger } from '@novacommerce/core-logger';
import { randomUUID } from 'crypto';

export interface AnalyticsEventInput {
  eventName: string;
  userId?: string;
  sessionId?: string;
  properties: Record<string, unknown>;
}

export class AnalyticsService {
  private readonly events: Array<AnalyticsEventInput & { id: string; timestamp: Date }> = [];
  private readonly logger: ILogger;

  constructor(logger: ILogger) {
    this.logger = logger.child({ component: 'AnalyticsService' });
  }

  public async trackEvent(input: AnalyticsEventInput): Promise<{ id: string; received: boolean }> {
    const id = randomUUID();
    this.events.push({
      ...input,
      id,
      timestamp: new Date()
    });
    this.logger.debug(`Tracked event: ${input.eventName}`, { eventId: id });
    return { id, received: true };
  }

  public getSummary() {
    const eventCounts: Record<string, number> = {};
    for (const ev of this.events) {
      eventCounts[ev.eventName] = (eventCounts[ev.eventName] || 0) + 1;
    }
    return {
      totalEvents: this.events.length,
      countsByEvent: eventCounts
    };
  }
}
