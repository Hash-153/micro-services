export interface ServiceRouteConfig {
  pathPrefix: string;
  targetUrl: string;
  timeoutMs: number;
  rateLimitRpm: number;
  requiresAuth: boolean;
  allowedRoles?: string[];
  circuitBreakerThreshold?: number;
  enableResponseCompression?: boolean;
}

export const GATEWAY_ROUTE_TABLE: ServiceRouteConfig[] = [
  { pathPrefix: '/api/v1/auth', targetUrl: 'http://auth-service:8001', timeoutMs: 5000, rateLimitRpm: 120, requiresAuth: false, circuitBreakerThreshold: 5, enableResponseCompression: true },
  { pathPrefix: '/api/v1/users', targetUrl: 'http://user-service:8002', timeoutMs: 5000, rateLimitRpm: 240, requiresAuth: true, circuitBreakerThreshold: 5, enableResponseCompression: true },
  { pathPrefix: '/api/v1/catalog', targetUrl: 'http://catalog-service:8003', timeoutMs: 3000, rateLimitRpm: 600, requiresAuth: false, circuitBreakerThreshold: 5, enableResponseCompression: true },
  { pathPrefix: '/api/v1/orders', targetUrl: 'http://order-service:8004', timeoutMs: 8000, rateLimitRpm: 180, requiresAuth: true, circuitBreakerThreshold: 5, enableResponseCompression: true },
  { pathPrefix: '/api/v1/payments', targetUrl: 'http://payment-service:8005', timeoutMs: 10000, rateLimitRpm: 120, requiresAuth: true, circuitBreakerThreshold: 5, enableResponseCompression: true },
  { pathPrefix: '/api/v1/fulfillment', targetUrl: 'http://fulfillment-service:8006', timeoutMs: 6000, rateLimitRpm: 180, requiresAuth: true, circuitBreakerThreshold: 5, enableResponseCompression: true },
  { pathPrefix: '/api/v1/notifications', targetUrl: 'http://notification-service:8007', timeoutMs: 5000, rateLimitRpm: 120, requiresAuth: true, circuitBreakerThreshold: 5, enableResponseCompression: true },
  { pathPrefix: '/api/v1/analytics', targetUrl: 'http://analytics-service:8008', timeoutMs: 3000, rateLimitRpm: 360, requiresAuth: true, circuitBreakerThreshold: 5, enableResponseCompression: true },
  { pathPrefix: '/api/v1/inventory', targetUrl: 'http://inventory-service:8009', timeoutMs: 4000, rateLimitRpm: 360, requiresAuth: true, circuitBreakerThreshold: 5, enableResponseCompression: true }
];
