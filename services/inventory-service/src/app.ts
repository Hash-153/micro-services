import express, { Express } from 'express';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware } from '@novacommerce/core-middleware';
import { InMemoryStockRepository, InMemoryReservationRepository } from './repositories/inventory.repository.js';
import { InventoryService } from './services/inventory.service.js';

export function createInventoryApp(): Express {
  const app = express();
  const logger = Logger.create('inventory-service');
  const service = new InventoryService(new InMemoryStockRepository(), new InMemoryReservationRepository());

  app.use(express.json());

  app.get('/health', (req, res) => res.json({ status: 'UP', service: 'inventory-service' }));

  app.post('/api/v1/inventory/stock', async (req, res, next) => {
    try {
      const { sku, warehouseId, quantity } = req.body;
      const stock = await service.setStock(sku, warehouseId || 'WH-MAIN-01', quantity);
      res.json({ success: true, data: stock });
    } catch (err) {
      next(err);
    }
  });

  app.post('/api/v1/inventory/reserve', async (req, res, next) => {
    try {
      const { orderId, sku, quantity } = req.body;
      const correlationId = req.headers['x-correlation-id'] as string;
      const reservation = await service.reserveStock(orderId, sku, quantity, correlationId);
      res.status(201).json({ success: true, data: reservation });
    } catch (err) {
      next(err);
    }
  });

  app.post('/api/v1/inventory/release', async (req, res, next) => {
    try {
      const { orderId } = req.body;
      const correlationId = req.headers['x-correlation-id'] as string;
      await service.releaseReservation(orderId, correlationId);
      res.json({ success: true, message: `Reservations for order ${orderId} released.` });
    } catch (err) {
      next(err);
    }
  });

  app.use(ErrorHandlerMiddleware.handle(logger));
  return app;
}
