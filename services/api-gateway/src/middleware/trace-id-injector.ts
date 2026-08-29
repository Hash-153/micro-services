import { Request, Response, NextFunction } from 'express';
import { W3cTraceContextPropagator } from '@novacommerce/core-logger';

export class TraceIdInjector {
  public static middleware() {
    return (req: Request, res: Response, next: NextFunction) => {
      const incoming = req.headers['traceparent'] as string | undefined;
      const parsed = W3cTraceContextPropagator.parse(incoming) || W3cTraceContextPropagator.generate();

      const traceparentHeader = W3cTraceContextPropagator.format(parsed);
      res.setHeader('traceparent', traceparentHeader);
      res.setHeader('X-Trace-Id', parsed.traceId);

      (req as any).traceContext = parsed;
      next();
    };
  }
}
