import { createGatewayApp } from './app.js';
import { GatewayConfig } from './config/gateway.config.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('api-gateway');
const app = createGatewayApp();

const server = app.listen(GatewayConfig.port, GatewayConfig.host, () => {
  logger.info(`NovaCommerce API Gateway listening on http://${GatewayConfig.host}:${GatewayConfig.port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down API Gateway gracefully...');
  server.close(() => {
    logger.info('API Gateway closed successfully.');
    process.exit(0);
  });
});
