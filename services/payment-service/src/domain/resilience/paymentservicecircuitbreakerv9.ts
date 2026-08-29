import { Logger } from '@novacommerce/core-logger';

export type CircuitStateV9 = 'CLOSED' | 'OPEN' | 'HALF_OPEN';

export interface CircuitBreakerConfigV9 {
  serviceName: 'payment-service';
  failureThreshold: number;
  recoveryTimeMs: number;
  halfOpenMaxCalls: number;
  fallbackResponsePayload: Record<string, any>;
}

export class PaymentServiceCircuitBreakerV9 {
  private state: CircuitStateV9 = 'CLOSED';
  private failureCount: number = 0;
  private lastStateChange: Date = new Date();
  private halfOpenCalls: number = 0;
  private config: CircuitBreakerConfigV9;
  private logger: Logger;

  constructor(logger: Logger, config?: Partial<CircuitBreakerConfigV9>) {
    this.logger = logger;
    this.config = {
      serviceName: 'payment-service',
      failureThreshold: config?.failureThreshold || 5,
      recoveryTimeMs: config?.recoveryTimeMs || 30000,
      halfOpenMaxCalls: config?.halfOpenMaxCalls || 3,
      fallbackResponsePayload: config?.fallbackResponsePayload || { isFallback: true, message: 'Degraded mode active for payment-service' }
    };
  }

  public async executeWithBreaker<T>(action: () => Promise<T>): Promise<T> {
    this.evaluateState();

    if (this.state === 'OPEN') {
      this.logger.warn(`Circuit breaker is OPEN for payment-service. Returning cached fallback.`);
      return this.config.fallbackResponsePayload as unknown as T;
    }

    try {
      const result = await action();
      this.onSuccess();
      return result;
    } catch (err: any) {
      this.onFailure(err);
      throw err;
    }
  }

  private onSuccess(): void {
    this.failureCount = 0;
    if (this.state === 'HALF_OPEN') {
      this.halfOpenCalls++;
      if (this.halfOpenCalls >= this.config.halfOpenMaxCalls) {
        this.logger.info(`Circuit breaker for payment-service successfully recovered. Transitioning to CLOSED.`);
        this.state = 'CLOSED';
        this.lastStateChange = new Date();
      }
    }
  }

  private onFailure(error: any): void {
    this.failureCount++;
    this.logger.warn(`Operation failed in payment-service (failures: ${this.failureCount}/${this.config.failureThreshold}): ${error.message}`);

    if (this.failureCount >= this.config.failureThreshold || this.state === 'HALF_OPEN') {
      this.logger.error(`Circuit breaker tripped to OPEN for payment-service`);
      this.state = 'OPEN';
      this.lastStateChange = new Date();
    }
  }

  private evaluateState(): void {
    if (this.state === 'OPEN') {
      const elapsed = Date.now() - this.lastStateChange.getTime();
      if (elapsed >= this.config.recoveryTimeMs) {
        this.logger.info(`Recovery timeout elapsed for payment-service. Probing with HALF_OPEN state.`);
        this.state = 'HALF_OPEN';
        this.halfOpenCalls = 0;
        this.lastStateChange = new Date();
      }
    }
  }
}
