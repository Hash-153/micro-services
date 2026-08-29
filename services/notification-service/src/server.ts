import { createNotificationApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('notification-service');
const port = parseInt(process.env.NOTIFICATION_SERVICE_PORT || '8007', 10);
const app = createNotificationApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce Notification Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down Notification Service gracefully...');
  server.close(() => process.exit(0));
});
