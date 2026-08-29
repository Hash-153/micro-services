import { Request, Response, NextFunction } from 'express';
import { Logger } from '@novacommerce/core-logger';

export type CircuitState = 'CLOSED' | 'OPEN' | 'HALF_OPEN';

export class ServiceCircuitBreaker {
  private name: string;
  private state: CircuitState = 'CLOSED';
  private failureCount: number = 0;
  private successCount: number = 0;
  private lastFailureTime: number = 0;
  private failureThreshold: number;
  private recoveryTimeMs: number;
  private logger: Logger;

  constructor(name: string, logger: Logger, failureThreshold: number = 5, recoveryTimeMs: number = 30000) {
    this.name = name;
    this.logger = logger;
    this.failureThreshold = failureThreshold;
    this.recoveryTimeMs = recoveryTimeMs;
  }

  public middleware() {
    return (req: Request, res: Response, next: NextFunction) => {
      if (this.state === 'OPEN') {
        const now = Date.now();
        if (now - this.lastFailureTime > this.recoveryTimeMs) {
          this.state = 'HALF_OPEN';
          this.logger.info(`Circuit breaker for ${this.name} entered HALF_OPEN state (probing downstream).`);
        } else {
          return res.status(503).json({
            success: false,
            statusCode: 503,
            error: {
              code: 'ERR_CIRCUIT_OPEN',
              message: `Service '${this.name}' is temporarily unavailable due to downstream failure protection.`,
              timestamp: new Date().toISOString()
            }
          });
        }
      }

      res.on('finish', () => {
        if (res.statusCode >= 500) {
          this.recordFailure();
        } else if (res.statusCode < 400) {
          this.recordSuccess();
        }
      });

      next();
    };
  }

  private recordFailure(): void {
    this.failureCount++;
    this.lastFailureTime = Date.now();

    if (this.state === 'HALF_OPEN' || this.failureCount >= this.failureThreshold) {
      this.state = 'OPEN';
      this.logger.error(`Circuit breaker for ${this.name} tripped to OPEN state after ${this.failureCount} failures.`);
    }
  }

  private recordSuccess(): void {
    if (this.state === 'HALF_OPEN') {
      this.successCount++;
      if (this.successCount >= 3) {
        this.state = 'CLOSED';
        this.failureCount = 0;
        this.successCount = 0;
        this.logger.info(`Circuit breaker for ${this.name} recovered to CLOSED state.`);
      }
    } else {
      this.failureCount = 0;
    }
  }
}
