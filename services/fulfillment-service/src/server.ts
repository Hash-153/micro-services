import { createFulfillmentApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('fulfillment-service');
const port = parseInt(process.env.FULFILLMENT_SERVICE_PORT || '8006', 10);
const app = createFulfillmentApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce Fulfillment Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down Fulfillment Service gracefully...');
  server.close(() => process.exit(0));
});
