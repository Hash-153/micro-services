import { Request, Response, NextFunction } from 'express';

export class CompressionNegotiator {
  public static middleware() {
    return (req: Request, res: Response, next: NextFunction) => {
      const acceptEncoding = req.headers['accept-encoding'] || '';

      if (typeof acceptEncoding === 'string') {
        if (acceptEncoding.includes('br')) {
          res.setHeader('X-Selected-Compression', 'brotli');
        } else if (acceptEncoding.includes('gzip')) {
          res.setHeader('X-Selected-Compression', 'gzip');
        } else if (acceptEncoding.includes('deflate')) {
          res.setHeader('X-Selected-Compression', 'deflate');
        }
      }

      next();
    };
  }
}
