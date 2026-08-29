import express, { Express, Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware, SlidingWindowRateLimiter } from '@novacommerce/core-middleware';
import { GatewayConfig } from './config/gateway.config.js';
import { randomUUID } from 'crypto';

export function createGatewayApp(): Express {
  const app = express();
  const logger = Logger.create('api-gateway');

  app.use(helmet());
  app.use(cors({ origin: '*' }));
  app.use(compression());
  app.use(express.json());

  // Correlation ID middleware
  app.use((req: Request, res: Response, next: NextFunction) => {
    const correlationId = (req.headers['x-correlation-id'] as string) || randomUUID();
    req.headers['x-correlation-id'] = correlationId;
    res.setHeader('x-correlation-id', correlationId);
    next();
  });

  // Global rate limiter
  const globalLimiter = new SlidingWindowRateLimiter(60000, 1000);
  app.use(globalLimiter.middleware());

  // Health and Readiness probes
  app.get('/health', (req: Request, res: Response) => {
    res.json({
      status: 'UP',
      service: 'api-gateway',
      timestamp: new Date().toISOString(),
      routesCount: GatewayConfig.routes.length
    });
  });

  app.get('/routes', (req: Request, res: Response) => {
    res.json({
      routes: GatewayConfig.routes.map(r => ({
        path: r.pathPrefix,
        authRequired: r.authRequired,
        rateLimit: r.rateLimitMax
      }))
    });
  });

  // Error handling
  app.use(ErrorHandlerMiddleware.handle(logger));

  return app;
}
