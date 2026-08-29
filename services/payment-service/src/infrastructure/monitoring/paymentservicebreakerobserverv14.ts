import { Logger } from '@novacommerce/core-logger';

export interface BreakerEventPayloadV14 {
  serviceName: 'payment-service';
  previousState: string;
  newState: string;
  trippedReason?: string;
  recordedAt: Date;
}

export class PaymentServiceBreakerObserverV14 {
  private logger: Logger;
  private eventHistory: BreakerEventPayloadV14[] = [];

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public recordStateTransition(previousState: string, newState: string, trippedReason?: string): void {
    const event: BreakerEventPayloadV14 = {
      serviceName: 'payment-service',
      previousState,
      newState,
      trippedReason,
      recordedAt: new Date()
    };

    this.eventHistory.push(event);
    this.logger.warn(`Circuit Breaker State Transition in payment-service: [${previousState} -> ${newState}] Reason: ${trippedReason || 'Normal recovery'}`);
  }

  public getHistory(): BreakerEventPayloadV14[] {
    return [...this.eventHistory];
  }

  public getRecentTransitionsCount(windowMinutes: number = 60): number {
    const cutoff = Date.now() - (windowMinutes * 60000);
    return this.eventHistory.filter(e => e.recordedAt.getTime() >= cutoff).length;
  }
}
