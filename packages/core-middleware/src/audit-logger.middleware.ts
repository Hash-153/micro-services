import { Request, Response, NextFunction } from 'express';
import { Logger } from '@novacommerce/core-logger';

export interface AuditRecord {
  service: string;
  method: string;
  path: string;
  statusCode: number;
  durationMs: number;
  userId?: string;
  ipAddress?: string;
  userAgent?: string;
  correlationId?: string;
  timestamp: string;
}

export function createAuditMiddleware(serviceName: string, logger: Logger) {
  return (req: Request, res: Response, next: NextFunction) => {
    const startTime = Date.now();
    const correlationId = (req.headers['x-correlation-id'] as string) || (req as any).correlationId;

    res.on('finish', () => {
      const durationMs = Date.now() - startTime;
      const user = (req as any).user;

      const record: AuditRecord = {
        service: serviceName,
        method: req.method,
        path: req.originalUrl || req.url,
        statusCode: res.statusCode,
        durationMs,
        userId: user?.id,
        ipAddress: req.ip || req.socket.remoteAddress,
        userAgent: req.get('user-agent'),
        correlationId,
        timestamp: new Date().toISOString()
      };

      if (res.statusCode >= 400) {
        logger.warn(`[AUDIT-WARN] ${record.method} ${record.path} ${record.statusCode} - ${durationMs}ms`, record);
      } else {
        logger.info(`[AUDIT] ${record.method} ${record.path} ${record.statusCode} - ${durationMs}ms`, record);
      }
    });

    next();
  };
}
