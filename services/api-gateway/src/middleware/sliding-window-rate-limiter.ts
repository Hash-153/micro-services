import { Request, Response, NextFunction } from 'express';
import { Logger } from '@novacommerce/core-logger';

export interface RateLimitRule {
  windowMs: number;
  maxRequests: number;
}

export class SlidingWindowRateLimiter {
  private requests: Map<string, number[]> = new Map();
  private logger: Logger;
  private rule: RateLimitRule;

  constructor(logger: Logger, rule: RateLimitRule = { windowMs: 60000, maxRequests: 120 }) {
    this.logger = logger;
    this.rule = rule;
  }

  public middleware() {
    return (req: Request, res: Response, next: NextFunction) => {
      const clientKey = req.ip || req.socket.remoteAddress || '127.0.0.1';
      const now = Date.now();
      const windowStart = now - this.rule.windowMs;

      const timestamps = (this.requests.get(clientKey) || []).filter(ts => ts > windowStart);

      if (timestamps.length >= this.rule.maxRequests) {
        res.setHeader('Retry-After', Math.ceil(this.rule.windowMs / 1000));
        return res.status(429).json({
          success: false,
          statusCode: 429,
          error: {
            code: 'ERR_TOO_MANY_REQUESTS',
            message: 'Too many requests, please slow down.',
            timestamp: new Date().toISOString()
          }
        });
      }

      timestamps.push(now);
      this.requests.set(clientKey, timestamps);

      res.setHeader('X-RateLimit-Limit', this.rule.maxRequests);
      res.setHeader('X-RateLimit-Remaining', this.rule.maxRequests - timestamps.length);

      next();
    };
  }
}
