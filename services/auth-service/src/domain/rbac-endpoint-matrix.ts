import { UserRole } from '@novacommerce/core-types';

export interface EndpointPermissionRule {
  endpointPath: string;
  httpMethod: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  allowedRoles: UserRole[];
  requiresMfa: boolean;
  rateLimitTier: 'STRICT' | 'STANDARD' | 'UNLIMITED';
}

export const RBAC_ENDPOINT_PERMISSION_RULES: EndpointPermissionRule[] = [
  // Auth endpoints
  { endpointPath: '/api/v1/auth/register', httpMethod: 'POST', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.CUSTOMER, UserRole.GUEST], requiresMfa: false, rateLimitTier: 'STRICT' },
  { endpointPath: '/api/v1/auth/login', httpMethod: 'POST', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATIONS_MANAGER, UserRole.FINANCE_ANALYST, UserRole.INVENTORY_MANAGER, UserRole.SUPPORT_AGENT, UserRole.CUSTOMER, UserRole.GUEST], requiresMfa: false, rateLimitTier: 'STRICT' },
  { endpointPath: '/api/v1/auth/refresh', httpMethod: 'POST', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATIONS_MANAGER, UserRole.FINANCE_ANALYST, UserRole.INVENTORY_MANAGER, UserRole.SUPPORT_AGENT, UserRole.CUSTOMER], requiresMfa: false, rateLimitTier: 'STANDARD' },
  { endpointPath: '/api/v1/auth/me', httpMethod: 'GET', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATIONS_MANAGER, UserRole.FINANCE_ANALYST, UserRole.INVENTORY_MANAGER, UserRole.SUPPORT_AGENT, UserRole.CUSTOMER], requiresMfa: false, rateLimitTier: 'STANDARD' },
  { endpointPath: '/api/v1/auth/mfa/setup', httpMethod: 'POST', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATIONS_MANAGER, UserRole.FINANCE_ANALYST, UserRole.INVENTORY_MANAGER, UserRole.SUPPORT_AGENT, UserRole.CUSTOMER], requiresMfa: false, rateLimitTier: 'STANDARD' },

  // User management endpoints
  { endpointPath: '/api/v1/users/profile', httpMethod: 'GET', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATIONS_MANAGER, UserRole.FINANCE_ANALYST, UserRole.INVENTORY_MANAGER, UserRole.SUPPORT_AGENT, UserRole.CUSTOMER], requiresMfa: false, rateLimitTier: 'STANDARD' },
  { endpointPath: '/api/v1/users/profile', httpMethod: 'PUT', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.CUSTOMER], requiresMfa: false, rateLimitTier: 'STANDARD' },
  { endpointPath: '/api/v1/users/addresses', httpMethod: 'GET', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.CUSTOMER], requiresMfa: false, rateLimitTier: 'STANDARD' },
  { endpointPath: '/api/v1/users/addresses', httpMethod: 'POST', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.CUSTOMER], requiresMfa: false, rateLimitTier: 'STANDARD' },

  // Catalog endpoints
  { endpointPath: '/api/v1/catalog/products', httpMethod: 'GET', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATIONS_MANAGER, UserRole.FINANCE_ANALYST, UserRole.INVENTORY_MANAGER, UserRole.SUPPORT_AGENT, UserRole.CUSTOMER, UserRole.GUEST], requiresMfa: false, rateLimitTier: 'UNLIMITED' },
  { endpointPath: '/api/v1/catalog/products', httpMethod: 'POST', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATIONS_MANAGER], requiresMfa: true, rateLimitTier: 'STANDARD' },
  { endpointPath: '/api/v1/catalog/products/:id', httpMethod: 'PUT', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATIONS_MANAGER], requiresMfa: true, rateLimitTier: 'STANDARD' },
  { endpointPath: '/api/v1/catalog/products/:id', httpMethod: 'DELETE', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN], requiresMfa: true, rateLimitTier: 'STRICT' },

  // Order endpoints
  { endpointPath: '/api/v1/orders', httpMethod: 'POST', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.CUSTOMER], requiresMfa: false, rateLimitTier: 'STANDARD' },
  { endpointPath: '/api/v1/orders', httpMethod: 'GET', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATIONS_MANAGER, UserRole.FINANCE_ANALYST, UserRole.CUSTOMER], requiresMfa: false, rateLimitTier: 'STANDARD' },
  { endpointPath: '/api/v1/orders/:id/cancel', httpMethod: 'POST', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATIONS_MANAGER, UserRole.SUPPORT_AGENT, UserRole.CUSTOMER], requiresMfa: false, rateLimitTier: 'STANDARD' },

  // Payment endpoints
  { endpointPath: '/api/v1/payments/authorize', httpMethod: 'POST', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.CUSTOMER, UserRole.SYSTEM_INTERNAL], requiresMfa: false, rateLimitTier: 'STANDARD' },
  { endpointPath: '/api/v1/payments/:id/capture', httpMethod: 'POST', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.FINANCE_ANALYST, UserRole.SYSTEM_INTERNAL], requiresMfa: false, rateLimitTier: 'STANDARD' },
  { endpointPath: '/api/v1/payments/:id/refund', httpMethod: 'POST', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.FINANCE_ANALYST, UserRole.SUPPORT_AGENT], requiresMfa: true, rateLimitTier: 'STRICT' },
  { endpointPath: '/api/v1/payments/ledger/reconcile', httpMethod: 'GET', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.FINANCE_ANALYST], requiresMfa: true, rateLimitTier: 'STANDARD' },

  // Inventory endpoints
  { endpointPath: '/api/v1/inventory/stock/:sku', httpMethod: 'GET', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATIONS_MANAGER, UserRole.INVENTORY_MANAGER, UserRole.CUSTOMER, UserRole.SYSTEM_INTERNAL], requiresMfa: false, rateLimitTier: 'UNLIMITED' },
  { endpointPath: '/api/v1/inventory/stock', httpMethod: 'POST', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.INVENTORY_MANAGER], requiresMfa: false, rateLimitTier: 'STANDARD' },
  { endpointPath: '/api/v1/inventory/reserve', httpMethod: 'POST', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.SYSTEM_INTERNAL], requiresMfa: false, rateLimitTier: 'STANDARD' },

  // Fulfillment endpoints
  { endpointPath: '/api/v1/fulfillment/shipments', httpMethod: 'POST', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATIONS_MANAGER, UserRole.SYSTEM_INTERNAL], requiresMfa: false, rateLimitTier: 'STANDARD' },
  { endpointPath: '/api/v1/fulfillment/rates', httpMethod: 'POST', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.CUSTOMER, UserRole.GUEST], requiresMfa: false, rateLimitTier: 'STANDARD' },

  // Analytics endpoints
  { endpointPath: '/api/v1/analytics/summary', httpMethod: 'GET', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATIONS_MANAGER, UserRole.FINANCE_ANALYST], requiresMfa: false, rateLimitTier: 'STANDARD' },
  { endpointPath: '/api/v1/analytics/revenue-rollup', httpMethod: 'GET', allowedRoles: [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.FINANCE_ANALYST], requiresMfa: true, rateLimitTier: 'STANDARD' }
];

export class RbacPermissionEvaluator {
  public static isAuthorized(path: string, method: string, role: UserRole): boolean {
    const rule = RBAC_ENDPOINT_PERMISSION_RULES.find(
      r => r.endpointPath === path && r.httpMethod.toUpperCase() === method.toUpperCase()
    );
    if (!rule) return true; // Default permit if not explicitly restricted
    return rule.allowedRoles.includes(role);
  }
}
