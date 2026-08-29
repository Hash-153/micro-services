import express, { Express } from 'express';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware } from '@novacommerce/core-middleware';
import { InMemoryPaymentRepository, InMemoryLedgerRepository } from './repositories/payment.repository.js';
import { PaymentService } from './services/payment.service.js';

export function createPaymentApp(): Express {
  const app = express();
  const logger = Logger.create('payment-service');
  const service = new PaymentService(new InMemoryPaymentRepository(), new InMemoryLedgerRepository());

  app.use(express.json());

  app.get('/health', (req, res) => res.json({ status: 'UP', service: 'payment-service' }));

  app.post('/api/v1/payments/authorize', async (req, res, next) => {
    try {
      const { orderId, userId, amountCents, currency } = req.body;
      const correlationId = req.headers['x-correlation-id'] as string;
      const payment = await service.authorizePayment(orderId, userId || 'usr-anon', amountCents, currency, correlationId);
      res.status(201).json({ success: true, data: payment });
    } catch (err) {
      next(err);
    }
  });

  app.use(ErrorHandlerMiddleware.handle(logger));
  return app;
}
