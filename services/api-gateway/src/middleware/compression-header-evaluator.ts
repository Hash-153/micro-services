import { Request, Response, NextFunction } from 'express';

export class CompressionHeaderEvaluator {
  public static selectBestEncoding(req: Request): 'br' | 'gzip' | 'deflate' | 'identity' {
    const acceptEncoding = req.headers['accept-encoding'] || '';

    if (typeof acceptEncoding === 'string') {
      if (acceptEncoding.includes('br')) return 'br';
      if (acceptEncoding.includes('gzip')) return 'gzip';
      if (acceptEncoding.includes('deflate')) return 'deflate';
    }

    return 'identity';
  }
}
