import { Logger } from '@novacommerce/core-logger';

export interface BreakerEventPayloadV15 {
  serviceName: 'user-service';
  previousState: string;
  newState: string;
  trippedReason?: string;
  recordedAt: Date;
}

export class UserServiceBreakerObserverV15 {
  private logger: Logger;
  private eventHistory: BreakerEventPayloadV15[] = [];

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public recordStateTransition(previousState: string, newState: string, trippedReason?: string): void {
    const event: BreakerEventPayloadV15 = {
      serviceName: 'user-service',
      previousState,
      newState,
      trippedReason,
      recordedAt: new Date()
    };

    this.eventHistory.push(event);
    this.logger.warn(`Circuit Breaker State Transition in user-service: [${previousState} -> ${newState}] Reason: ${trippedReason || 'Normal recovery'}`);
  }

  public getHistory(): BreakerEventPayloadV15[] {
    return [...this.eventHistory];
  }

  public getRecentTransitionsCount(windowMinutes: number = 60): number {
    const cutoff = Date.now() - (windowMinutes * 60000);
    return this.eventHistory.filter(e => e.recordedAt.getTime() >= cutoff).length;
  }
}
