import { createInventoryApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('inventory-service');
const port = parseInt(process.env.INVENTORY_SERVICE_PORT || '8009', 10);
const app = createInventoryApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce Inventory Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down Inventory Service gracefully...');
  server.close(() => process.exit(0));
});
