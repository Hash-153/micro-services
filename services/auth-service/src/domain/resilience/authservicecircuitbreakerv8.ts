import { Logger } from '@novacommerce/core-logger';

export type CircuitStateV8 = 'CLOSED' | 'OPEN' | 'HALF_OPEN';

export interface CircuitBreakerConfigV8 {
  serviceName: 'auth-service';
  failureThreshold: number;
  recoveryTimeMs: number;
  halfOpenMaxCalls: number;
  fallbackResponsePayload: Record<string, any>;
}

export class AuthServiceCircuitBreakerV8 {
  private state: CircuitStateV8 = 'CLOSED';
  private failureCount: number = 0;
  private lastStateChange: Date = new Date();
  private halfOpenCalls: number = 0;
  private config: CircuitBreakerConfigV8;
  private logger: Logger;

  constructor(logger: Logger, config?: Partial<CircuitBreakerConfigV8>) {
    this.logger = logger;
    this.config = {
      serviceName: 'auth-service',
      failureThreshold: config?.failureThreshold || 5,
      recoveryTimeMs: config?.recoveryTimeMs || 30000,
      halfOpenMaxCalls: config?.halfOpenMaxCalls || 3,
      fallbackResponsePayload: config?.fallbackResponsePayload || { isFallback: true, message: 'Degraded mode active for auth-service' }
    };
  }

  public async executeWithBreaker<T>(action: () => Promise<T>): Promise<T> {
    this.evaluateState();

    if (this.state === 'OPEN') {
      this.logger.warn(`Circuit breaker is OPEN for auth-service. Returning cached fallback.`);
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
        this.logger.info(`Circuit breaker for auth-service successfully recovered. Transitioning to CLOSED.`);
        this.state = 'CLOSED';
        this.lastStateChange = new Date();
      }
    }
  }

  private onFailure(error: any): void {
    this.failureCount++;
    this.logger.warn(`Operation failed in auth-service (failures: ${this.failureCount}/${this.config.failureThreshold}): ${error.message}`);

    if (this.failureCount >= this.config.failureThreshold || this.state === 'HALF_OPEN') {
      this.logger.error(`Circuit breaker tripped to OPEN for auth-service`);
      this.state = 'OPEN';
      this.lastStateChange = new Date();
    }
  }

  private evaluateState(): void {
    if (this.state === 'OPEN') {
      const elapsed = Date.now() - this.lastStateChange.getTime();
      if (elapsed >= this.config.recoveryTimeMs) {
        this.logger.info(`Recovery timeout elapsed for auth-service. Probing with HALF_OPEN state.`);
        this.state = 'HALF_OPEN';
        this.halfOpenCalls = 0;
        this.lastStateChange = new Date();
      }
    }
  }
}
