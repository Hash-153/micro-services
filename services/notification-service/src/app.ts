import express, { Express } from 'express';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware } from '@novacommerce/core-middleware';
import { NotificationService } from './services/notification.service.js';

export function createNotificationApp(): Express {
  const app = express();
  const logger = Logger.create('notification-service');
  const service = new NotificationService(logger);

  app.use(express.json());

  app.get('/health', (req, res) => res.json({ status: 'UP', service: 'notification-service' }));

  app.post('/api/v1/notifications/send', async (req, res, next) => {
    try {
      const result = await service.send(req.body);
      res.status(202).json({ success: true, data: result });
    } catch (err) {
      next(err);
    }
  });

  app.use(ErrorHandlerMiddleware.handle(logger));
  return app;
}
