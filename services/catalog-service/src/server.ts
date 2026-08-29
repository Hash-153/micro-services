import { createCatalogApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('catalog-service');
const port = parseInt(process.env.CATALOG_SERVICE_PORT || '8003', 10);
const app = createCatalogApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce Catalog Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down Catalog Service gracefully...');
  server.close(() => process.exit(0));
});
