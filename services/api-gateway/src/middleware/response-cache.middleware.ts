import { Request, Response, NextFunction } from 'express';
import { Logger } from '@novacommerce/core-logger';

export class ResponseCacheMiddleware {
  private cache: Map<string, { body: any; headers: Record<string, any>; expiresAt: number }> = new Map();
  private logger: Logger;
  private defaultTtlSeconds: number;

  constructor(logger: Logger, defaultTtlSeconds: number = 60) {
    this.logger = logger;
    this.defaultTtlSeconds = defaultTtlSeconds;
  }

  public middleware() {
    return (req: Request, res: Response, next: NextFunction) => {
      if (req.method !== 'GET') {
        return next();
      }

      const cacheKey = `${req.originalUrl || req.url}`;
      const cached = this.cache.get(cacheKey);

      if (cached && Date.now() < cached.expiresAt) {
        res.setHeader('X-Cache-Status', 'HIT');
        return res.json(cached.body);
      }

      res.setHeader('X-Cache-Status', 'MISS');
      const originalJson = res.json.bind(res);

      res.json = (body: any) => {
        if (res.statusCode === 200) {
          this.cache.set(cacheKey, {
            body,
            headers: {},
            expiresAt: Date.now() + this.defaultTtlSeconds * 1000
          });
        }
        return originalJson(body);
      };

      next();
    };
  }

  public clear(): void {
    this.cache.clear();
  }
}
