import { createUserApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('user-service');
const port = parseInt(process.env.USER_SERVICE_PORT || '8002', 10);
const app = createUserApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce User Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down User Service gracefully...');
  server.close(() => process.exit(0));
});
