import { createAuthApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('auth-service');
const port = parseInt(process.env.AUTH_SERVICE_PORT || '8001', 10);
const app = createAuthApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce Auth Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down Auth Service gracefully...');
  server.close(() => process.exit(0));
});
