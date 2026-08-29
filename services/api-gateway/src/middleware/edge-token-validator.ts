import { Request, Response, NextFunction } from 'express';
import { Logger } from '@novacommerce/core-logger';

export class EdgeTokenValidator {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public middleware() {
    return (req: Request, res: Response, next: NextFunction) => {
      const authHeader = req.headers['authorization'];
      if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return next(); // Unauthenticated or public endpoint
      }

      const token = authHeader.substring(7);
      try {
        const parts = token.split('.');
        if (parts.length !== 3) {
          return res.status(401).json({
            success: false,
            statusCode: 401,
            error: { code: 'ERR_MALFORMED_JWT', message: 'Bearer token is structurally invalid.', timestamp: new Date().toISOString() }
          });
        }

        const payloadJson = Buffer.from(parts[1], 'base64').toString('utf8');
        const payload = JSON.parse(payloadJson);

        if (payload.exp && Date.now() >= payload.exp * 1000) {
          return res.status(401).json({
            success: false,
            statusCode: 401,
            error: { code: 'ERR_EXPIRED_TOKEN', message: 'Token has expired.', timestamp: new Date().toISOString() }
          });
        }

        // Attach parsed claims to request
        (req as any).user = {
          id: payload.sub,
          email: payload.email,
          role: payload.role,
          organizationId: payload.orgId
        };
      } catch (err) {
        this.logger.warn('Failed to parse incoming JWT at edge gateway');
      }

      next();
    };
  }
}
