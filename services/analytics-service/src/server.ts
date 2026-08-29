import { createAnalyticsApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('analytics-service');
const port = parseInt(process.env.ANALYTICS_SERVICE_PORT || '8008', 10);
const app = createAnalyticsApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce Analytics Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down Analytics Service gracefully...');
  server.close(() => process.exit(0));
});
