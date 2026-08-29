import { ServiceCircuitBreaker } from './circuit-breaker.middleware.js';
import { Logger } from '@novacommerce/core-logger';

export class CircuitBreakerRegistry {
  private breakers: Map<string, ServiceCircuitBreaker> = new Map();
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public getOrCreate(serviceName: string, failureThreshold: number = 5, recoveryTimeMs: number = 30000): ServiceCircuitBreaker {
    if (!this.breakers.has(serviceName)) {
      const cb = new ServiceCircuitBreaker(serviceName, this.logger, failureThreshold, recoveryTimeMs);
      this.breakers.set(serviceName, cb);
    }
    return this.breakers.get(serviceName)!;
  }
}
