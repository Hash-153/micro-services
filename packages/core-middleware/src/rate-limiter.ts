import { AppError, ErrorCode } from '@novacommerce/core-types';

export class SlidingWindowRateLimiter {
  private readonly windowMs: number;
  private readonly maxRequests: number;
  private readonly clientRequests: Map<string, number[]> = new Map();

  constructor(windowMs: number = 60000, maxRequests: number = 100) {
    this.windowMs = windowMs;
    this.maxRequests = maxRequests;
  }

  public middleware() {
    return (req: any, res: any, next: any) => {
      const clientIp = req.ip || req.headers['x-forwarded-for'] || '127.0.0.1';
      const now = Date.now();
      const windowStart = now - this.windowMs;

      let timestamps = this.clientRequests.get(clientIp) || [];
      timestamps = timestamps.filter(ts => ts > windowStart);

      if (timestamps.length >= this.maxRequests) {
        return next(
          new AppError(
            `Rate limit exceeded. Maximum ${this.maxRequests} requests per ${this.windowMs / 1000}s.`,
            429,
            ErrorCode.RATE_LIMIT_EXCEEDED
          )
        );
      }

      timestamps.push(now);
      this.clientRequests.set(clientIp, timestamps);
      return next();
    };
  }
}
