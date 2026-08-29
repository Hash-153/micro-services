import express, { Express } from 'express';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware } from '@novacommerce/core-middleware';
import { AnalyticsService } from './services/analytics.service.js';

export function createAnalyticsApp(): Express {
  const app = express();
  const logger = Logger.create('analytics-service');
  const service = new AnalyticsService(logger);

  app.use(express.json());

  app.get('/health', (req, res) => res.json({ status: 'UP', service: 'analytics-service' }));

  app.post('/api/v1/analytics/events', async (req, res, next) => {
    try {
      const result = await service.trackEvent(req.body);
      res.status(202).json({ success: true, data: result });
    } catch (err) {
      next(err);
    }
  });

  app.get('/api/v1/analytics/summary', (req, res) => {
    res.json({ success: true, data: service.getSummary() });
  });

  app.use(ErrorHandlerMiddleware.handle(logger));
  return app;
}
