import { createOrderApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('order-service');
const port = parseInt(process.env.ORDER_SERVICE_PORT || '8004', 10);
const app = createOrderApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce Order Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down Order Service gracefully...');
  server.close(() => process.exit(0));
});
