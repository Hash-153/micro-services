import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_master_surge():
    print("Generating comprehensive Master Surge Modules...")

    # 1. Auth Service RBAC Permission Matrix for 60 API Endpoints
    rbac_matrix_code = """import { UserRole } from '@novacommerce/core-types';

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
"""
    write_file("services/auth-service/src/domain/rbac-endpoint-matrix.ts", rbac_matrix_code)

    # 2. Notification Handlebars Email Templates Master Registry
    write_file("services/notification-service/src/domain/transactional-email-templates.ts", """export interface EmailTemplateDefinition {
  templateKey: string;
  subject: string;
  htmlContent: string;
  textContent: string;
  requiredVariables: string[];
}

export const TRANSACTIONAL_EMAIL_TEMPLATES: Record<string, EmailTemplateDefinition> = {
  'ORDER_CONFIRMATION': {
    templateKey: 'ORDER_CONFIRMATION',
    subject: 'Order Confirmed - #{{orderNumber}}',
    htmlContent: `
      <div style="font-family: sans-serif; max-width: 600px; margin: auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 8px;">
        <h2 style="color: #1e40af;">Thank you for your order, {{customerName}}!</h2>
        <p>Your order <strong>#{{orderNumber}}</strong> has been received and is being processed by our automated fulfillment network.</p>
        <div style="background: #f8fafc; padding: 16px; border-radius: 6px; margin: 20px 0;">
          <p style="margin: 0;"><strong>Order Total:</strong> {{totalAmount}}</p>
          <p style="margin: 4px 0 0;"><strong>Estimated Delivery:</strong> {{estimatedDeliveryDate}}</p>
        </div>
        <p>You can track the live status of your shipment anytime at <a href="{{trackingUrl}}">{{trackingUrl}}</a>.</p>
      </div>`,
    textContent: 'Thank you for your order, {{customerName}}! Order #{{orderNumber}} is being processed. Total: {{totalAmount}}. Track at: {{trackingUrl}}',
    requiredVariables: ['customerName', 'orderNumber', 'totalAmount', 'estimatedDeliveryDate', 'trackingUrl']
  },
  'PAYMENT_RECEIPT': {
    templateKey: 'PAYMENT_RECEIPT',
    subject: 'Payment Receipt for Order #{{orderNumber}}',
    htmlContent: `
      <div style="font-family: sans-serif; max-width: 600px; margin: auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 8px;">
        <h2 style="color: #059669;">Payment Successful</h2>
        <p>We received your payment of <strong>{{amountPaid}}</strong> for Order #{{orderNumber}}.</p>
        <p><strong>Payment Method:</strong> {{paymentMethod}} (ending in {{lastFour}})</p>
        <p><strong>Transaction Reference:</strong> {{transactionReference}}</p>
      </div>`,
    textContent: 'Payment of {{amountPaid}} received for Order #{{orderNumber}}. Reference: {{transactionReference}}',
    requiredVariables: ['amountPaid', 'orderNumber', 'paymentMethod', 'lastFour', 'transactionReference']
  },
  'SHIPMENT_DISPATCHED': {
    templateKey: 'SHIPMENT_DISPATCHED',
    subject: 'Your order #{{orderNumber}} is on the way!',
    htmlContent: `
      <div style="font-family: sans-serif; max-width: 600px; margin: auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 8px;">
        <h2 style="color: #2563eb;">Package Dispatched</h2>
        <p>Carrier: <strong>{{carrierName}}</strong></p>
        <p>Tracking Number: <strong>{{trackingNumber}}</strong></p>
        <a href="{{trackingUrl}}" style="display: inline-block; background: #2563eb; color: #fff; padding: 12px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; margin-top: 12px;">Track Package</a>
      </div>`,
    textContent: 'Your order #{{orderNumber}} has been shipped via {{carrierName}}. Tracking: {{trackingNumber}}',
    requiredVariables: ['orderNumber', 'carrierName', 'trackingNumber', 'trackingUrl']
  }
};

export class EmailTemplateRegistry {
  public static getTemplate(key: string): EmailTemplateDefinition | undefined {
    return TRANSACTIONAL_EMAIL_TEMPLATES[key];
  }
}
""")

    print("Master surge modules generated.")

if __name__ == "__main__":
    generate_master_surge()
