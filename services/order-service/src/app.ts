import express, { Express } from 'express';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware, RequestValidator } from '@novacommerce/core-middleware';
import { InMemoryOrderRepository } from './repositories/order.repository.js';
import { OrderService } from './services/order.service.js';
import { CreateOrderSchema } from '@novacommerce/core-types';

export function createOrderApp(): Express {
  const app = express();
  const logger = Logger.create('order-service');
  const service = new OrderService(new InMemoryOrderRepository());

  app.use(express.json());

  app.get('/health', (req, res) => res.json({ status: 'UP', service: 'order-service' }));

  app.post('/api/v1/orders', RequestValidator.validateBody(CreateOrderSchema), async (req, res, next) => {
    try {
      const correlationId = req.headers['x-correlation-id'] as string;
      const order = await service.createOrder(req.body, req.body.userId || 'usr-default', correlationId);
      res.status(201).json({ success: true, data: order });
    } catch (err) {
      next(err);
    }
  });

  app.get('/api/v1/orders/:id', async (req, res, next) => {
    try {
      const order = await service.getOrderById(req.params.id);
      res.json({ success: true, data: order });
    } catch (err) {
      next(err);
    }
  });

  app.use(ErrorHandlerMiddleware.handle(logger));
  return app;
}
