import express, { Express } from 'express';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware } from '@novacommerce/core-middleware';
import { InMemoryShipmentRepository } from './repositories/shipment.repository.js';
import { FulfillmentService } from './services/fulfillment.service.js';

export function createFulfillmentApp(): Express {
  const app = express();
  const logger = Logger.create('fulfillment-service');
  const service = new FulfillmentService(new InMemoryShipmentRepository());

  app.use(express.json());

  app.get('/health', (req, res) => res.json({ status: 'UP', service: 'fulfillment-service' }));

  app.post('/api/v1/fulfillment/shipments', async (req, res, next) => {
    try {
      const { orderId, destinationAddress, carrier } = req.body;
      const correlationId = req.headers['x-correlation-id'] as string;
      const shipment = await service.createShipment(orderId, destinationAddress || {}, carrier, correlationId);
      res.status(201).json({ success: true, data: shipment });
    } catch (err) {
      next(err);
    }
  });

  app.use(ErrorHandlerMiddleware.handle(logger));
  return app;
}
