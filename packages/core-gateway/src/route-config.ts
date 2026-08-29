export interface RouteConfig {
  path: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  service: string;
  targetPath: string;
  authRequired: boolean;
  rateLimit?: {
    requests: number;
    windowMs: number;
  };
  cacheConfig?: {
    enabled: boolean;
    ttlSeconds: number;
  };
  validation?: {
    schema: any;
    strict: boolean;
  };
}

export class RouteConfigManager {
  private routes: Map<string, RouteConfig[]> = new Map();

  constructor() {
    this.initializeDefaultRoutes();
  }

  private initializeDefaultRoutes(): void {
    // Auth service routes
    this.addRoute('auth', {
      path: '/api/v1/auth/register',
      method: 'POST',
      service: 'auth-service',
      targetPath: '/register',
      authRequired: false,
      rateLimit: { requests: 10, windowMs: 60000 },
      validation: { schema: null, strict: true }
    });

    this.addRoute('auth', {
      path: '/api/v1/auth/login',
      method: 'POST',
      service: 'auth-service',
      targetPath: '/login',
      authRequired: false,
      rateLimit: { requests: 5, windowMs: 60000 },
      validation: { schema: null, strict: true }
    });

    this.addRoute('auth', {
      path: '/api/v1/auth/logout',
      method: 'POST',
      service: 'auth-service',
      targetPath: '/logout',
      authRequired: true,
      rateLimit: { requests: 20, windowMs: 60000 }
    });

    // Catalog service routes
    this.addRoute('catalog', {
      path: '/api/v1/catalog/products',
      method: 'GET',
      service: 'catalog-service',
      targetPath: '/products',
      authRequired: false,
      cacheConfig: { enabled: true, ttlSeconds: 300 },
      rateLimit: { requests: 100, windowMs: 60000 }
    });

    this.addRoute('catalog', {
      path: '/api/v1/catalog/products/:id',
      method: 'GET',
      service: 'catalog-service',
      targetPath: '/products/:id',
      authRequired: false,
      cacheConfig: { enabled: true, ttlSeconds: 600 },
      rateLimit: { requests: 50, windowMs: 60000 }
    });

    this.addRoute('catalog', {
      path: '/api/v1/catalog/search',
      method: 'GET',
      service: 'catalog-service',
      targetPath: '/search',
      authRequired: false,
      cacheConfig: { enabled: true, ttlSeconds: 180 },
      rateLimit: { requests: 30, windowMs: 60000 }
    });

    // Order service routes
    this.addRoute('orders', {
      path: '/api/v1/orders',
      method: 'POST',
      service: 'order-service',
      targetPath: '/orders',
      authRequired: true,
      rateLimit: { requests: 10, windowMs: 60000 },
      validation: { schema: null, strict: true }
    });

    this.addRoute('orders', {
      path: '/api/v1/orders/:id',
      method: 'GET',
      service: 'order-service',
      targetPath: '/orders/:id',
      authRequired: true,
      cacheConfig: { enabled: true, ttlSeconds: 120 }
    });

    this.addRoute('orders', {
      path: '/api/v1/orders/:id/cancel',
      method: 'POST',
      service: 'order-service',
      targetPath: '/orders/:id/cancel',
      authRequired: true,
      rateLimit: { requests: 5, windowMs: 60000 }
    });

    // Payment service routes
    this.addRoute('payments', {
      path: '/api/v1/payments',
      method: 'POST',
      service: 'payment-service',
      targetPath: '/payments',
      authRequired: true,
      rateLimit: { requests: 10, windowMs: 60000 },
      validation: { schema: null, strict: true }
    });

    this.addRoute('payments', {
      path: '/api/v1/payments/:id/refund',
      method: 'POST',
      service: 'payment-service',
      targetPath: '/payments/:id/refund',
      authRequired: true,
      rateLimit: { requests: 5, windowMs: 60000 }
    });

    // Inventory service routes
    this.addRoute('inventory', {
      path: '/api/v1/inventory/stock/:sku',
      method: 'GET',
      service: 'inventory-service',
      targetPath: '/stock/:sku',
      authRequired: false,
      cacheConfig: { enabled: true, ttlSeconds: 60 },
      rateLimit: { requests: 50, windowMs: 60000 }
    });

    this.addRoute('inventory', {
      path: '/api/v1/inventory/reserve',
      method: 'POST',
      service: 'inventory-service',
      targetPath: '/reserve',
      authRequired: true,
      rateLimit: { requests: 20, windowMs: 60000 }
    });

    // Shipping service routes
    this.addRoute('shipping', {
      path: '/api/v1/shipping/rates',
      method: 'POST',
      service: 'shipping-service',
      targetPath: '/rates',
      authRequired: false,
      cacheConfig: { enabled: true, ttlSeconds: 300 },
      rateLimit: { requests: 30, windowMs: 60000 }
    });

    this.addRoute('shipping', {
      path: '/api/v1/shipping/shipments',
      method: 'POST',
      service: 'shipping-service',
      targetPath: '/shipments',
      authRequired: true,
      rateLimit: { requests: 20, windowMs: 60000 }
    });

    this.addRoute('shipping', {
      path: '/api/v1/shipping/track/:trackingNumber',
      method: 'GET',
      service: 'shipping-service',
      targetPath: '/track/:trackingNumber',
      authRequired: false,
      cacheConfig: { enabled: true, ttlSeconds: 300 },
      rateLimit: { requests: 50, windowMs: 60000 }
    });
  }

  public addRoute(group: string, config: RouteConfig): void {
    if (!this.routes.has(group)) {
      this.routes.set(group, []);
    }
    this.routes.get(group)!.push(config);
  }

  public getRoutes(group: string): RouteConfig[] {
    return this.routes.get(group) || [];
  }

  public getAllRoutes(): RouteConfig[] {
    const allRoutes: RouteConfig[] = [];
    for (const routes of this.routes.values()) {
      allRoutes.push(...routes);
    }
    return allRoutes;
  }

  public findRoute(path: string, method: string): RouteConfig | null {
    for (const routes of this.routes.values()) {
      for (const route of routes) {
        if (this.matchPath(route.path, path) && route.method === method) {
          return route;
        }
      }
    }
    return null;
  }

  private matchPath(routePath: string, requestPath: string): boolean {
    // Simple path matching - in production, use proper path-to-regexp
    const routePattern = routePath.replace(/:([^/]+)/g, '([^/]+)');
    const regex = new RegExp(`^${routePattern}$`);
    return regex.test(requestPath);
  }
}
