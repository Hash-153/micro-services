import crypto from 'crypto';
import { Request, Response, NextFunction } from 'express';

export class HmacSignatureValidator {
  public static middleware(sharedSecret: string) {
    return (req: Request, res: Response, next: NextFunction) => {
      const signatureHeader = req.headers['x-hmac-signature'] as string | undefined;
      const timestampHeader = req.headers['x-hmac-timestamp'] as string | undefined;

      if (!signatureHeader || !timestampHeader) {
        return res.status(401).json({
          success: false,
          statusCode: 401,
          error: { code: 'ERR_MISSING_SIGNATURE', message: 'HMAC signature or timestamp header is missing.' }
        });
      }

      const reqTime = parseInt(timestampHeader, 10);
      if (Math.abs(Date.now() - reqTime) > 300000) { // 5-minute replay window
        return res.status(401).json({
          success: false,
          statusCode: 401,
          error: { code: 'ERR_TIMESTAMP_EXPIRED', message: 'HMAC timestamp signature is expired or skewed.' }
        });
      }

      const bodyStr = req.body ? JSON.stringify(req.body) : '';
      const payload = `${req.method}|${req.originalUrl || req.url}|${timestampHeader}|${bodyStr}`;
      const expected = crypto.createHmac('sha256', sharedSecret).update(payload).digest('hex');

      if (!crypto.timingSafeEqual(Buffer.from(signatureHeader), Buffer.from(expected))) {
        return res.status(403).json({
          success: false,
          statusCode: 403,
          error: { code: 'ERR_INVALID_SIGNATURE', message: 'HMAC signature mismatch.' }
        });
      }

      next();
    };
  }
}
