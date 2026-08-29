export interface GatewayRoute {
  pathPrefix: string;
  targetUrl: string;
  authRequired: boolean;
  rateLimitMax: number;
}

export const GatewayConfig = {
  port: parseInt(process.env.GATEWAY_PORT || '8000', 10),
  host: process.env.GATEWAY_HOST || '0.0.0.0',
  jwtSecret: process.env.JWT_SECRET || 'super_secret_local_jwt_signing_key_min_32_characters_long',
  routes: [
    {
      pathPrefix: '/api/v1/auth',
      targetUrl: process.env.AUTH_SERVICE_URL || 'http://localhost:8001',
      authRequired: false,
      rateLimitMax: 100
    },
    {
      pathPrefix: '/api/v1/users',
      targetUrl: process.env.USER_SERVICE_URL || 'http://localhost:8002',
      authRequired: true,
      rateLimitMax: 200
    },
    {
      pathPrefix: '/api/v1/catalog',
      targetUrl: process.env.CATALOG_SERVICE_URL || 'http://localhost:8003',
      authRequired: false,
      rateLimitMax: 500
    },
    {
      pathPrefix: '/api/v1/orders',
      targetUrl: process.env.ORDER_SERVICE_URL || 'http://localhost:8004',
      authRequired: true,
      rateLimitMax: 150
    },
    {
      pathPrefix: '/api/v1/payments',
      targetUrl: process.env.PAYMENT_SERVICE_URL || 'http://localhost:8005',
      authRequired: true,
      rateLimitMax: 100
    },
    {
      pathPrefix: '/api/v1/fulfillment',
      targetUrl: process.env.FULFILLMENT_SERVICE_URL || 'http://localhost:8006',
      authRequired: true,
      rateLimitMax: 150
    },
    {
      pathPrefix: '/api/v1/notifications',
      targetUrl: process.env.NOTIFICATION_SERVICE_URL || 'http://localhost:8007',
      authRequired: true,
      rateLimitMax: 100
    },
    {
      pathPrefix: '/api/v1/analytics',
      targetUrl: process.env.ANALYTICS_SERVICE_URL || 'http://localhost:8008',
      authRequired: true,
      rateLimitMax: 300
    },
    {
      pathPrefix: '/api/v1/inventory',
      targetUrl: process.env.INVENTORY_SERVICE_URL || 'http://localhost:8009',
      authRequired: true,
      rateLimitMax: 300
    }
  ]
};
