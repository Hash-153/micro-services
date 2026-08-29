import { Request, Response, NextFunction } from 'express';

export function responseCompressorMiddleware() {
  return (req: Request, res: Response, next: NextFunction) => {
    const acceptEncoding = req.headers['accept-encoding'] || '';
    if (typeof acceptEncoding === 'string' && acceptEncoding.includes('gzip')) {
      res.setHeader('Vary', 'Accept-Encoding');
    }
    next();
  };
}
