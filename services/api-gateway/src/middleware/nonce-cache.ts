import { Request, Response, NextFunction } from 'express';

export class NonceCacheMiddleware {
  private static nonces: Map<string, number> = new Map(); // nonce -> expiry timestamp

  public static middleware(ttlSeconds: number = 300) {
    return (req: Request, res: Response, next: NextFunction) => {
      const nonce = req.headers['x-request-nonce'] as string | undefined;
      if (!nonce) {
        return next(); // Nonce not required for all endpoints
      }

      const now = Date.now();
      const existing = this.nonces.get(nonce);

      if (existing && existing > now) {
        return res.status(409).json({
          success: false,
          statusCode: 409,
          error: { code: 'ERR_DUPLICATE_NONCE', message: 'Request nonce has already been consumed.' }
        });
      }

      this.nonces.set(nonce, now + ttlSeconds * 1000);
      next();
    };
  }
}
