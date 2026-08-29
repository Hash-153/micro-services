import crypto from 'crypto';
import { Request, Response, NextFunction } from 'express';

export class EtagCacheValidator {
  public static middleware() {
    return (req: Request, res: Response, next: NextFunction) => {
      if (req.method !== 'GET' && req.method !== 'HEAD') {
        return next();
      }

      const originalSend = res.send.bind(res);
      res.send = (body: any): Response => {
        if (body) {
          const content = typeof body === 'string' ? body : JSON.stringify(body);
          const etag = `W/"${crypto.createHash('sha1').update(content).digest('hex').slice(0, 16)}"`;
          res.setHeader('ETag', etag);

          const clientEtag = req.headers['if-none-match'];
          if (clientEtag === etag) {
            return res.status(304).end();
          }
        }
        return originalSend(body);
      };

      next();
    };
  }
}
