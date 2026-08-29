import { createPaymentApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('payment-service');
const port = parseInt(process.env.PAYMENT_SERVICE_PORT || '8005', 10);
const app = createPaymentApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce Payment Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down Payment Service gracefully...');
  server.close(() => process.exit(0));
});
