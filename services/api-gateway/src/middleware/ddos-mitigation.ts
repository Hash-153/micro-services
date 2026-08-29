import { Request, Response, NextFunction } from 'express';
import { Logger } from '@novacommerce/core-logger';

export class DdosMitigationGuard {
  private ipConnections: Map<string, number> = new Map();
  private maxConcurrentPerIp: number;
  private logger: Logger;

  constructor(logger: Logger, maxConcurrentPerIp: number = 50) {
    this.logger = logger;
    this.maxConcurrentPerIp = maxConcurrentPerIp;
  }

  public middleware() {
    return (req: Request, res: Response, next: NextFunction) => {
      const ip = req.ip || req.socket.remoteAddress || '127.0.0.1';
      const current = this.ipConnections.get(ip) || 0;

      if (current >= this.maxConcurrentPerIp) {
        this.logger.warn(`DDoS mitigation: dropped concurrent connection flood from IP ${ip} (${current} active)`);
        return res.status(429).json({
          success: false,
          statusCode: 429,
          error: { code: 'ERR_CONCURRENT_LIMIT_EXCEEDED', message: 'Too many concurrent socket connections from this IP.' }
        });
      }

      this.ipConnections.set(ip, current + 1);

      res.on('finish', () => {
        const count = this.ipConnections.get(ip) || 1;
        if (count <= 1) {
          this.ipConnections.delete(ip);
        } else {
          this.ipConnections.set(ip, count - 1);
        }
      });

      next();
    };
  }
}
