import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_deep_services_and_tests():
    # 1. Auth Service: MFA & RBAC Engine
    write_file("services/auth-service/src/services/mfa.service.ts", """import { createHmac, randomBytes } from 'crypto';

export interface MfaSetupResult {
  secret: string;
  otpauthUrl: string;
  backupCodes: string[];
}

export class MfaService {
  public static generateSecret(userEmail: string, issuer: string = 'NovaCommerce'): MfaSetupResult {
    const secret = randomBytes(20).toString('hex').toUpperCase().substring(0, 32);
    const otpauthUrl = `otpauth://totp/${encodeURIComponent(issuer)}:${encodeURIComponent(userEmail)}?secret=${secret}&issuer=${encodeURIComponent(issuer)}&algorithm=SHA1&digits=6&period=30`;
    
    const backupCodes: string[] = [];
    for (let i = 0; i < 8; i++) {
      backupCodes.push(randomBytes(4).toString('hex').toUpperCase());
    }

    return { secret, otpauthUrl, backupCodes };
  }

  public static verifyCode(secret: string, code: string, windowSteps: number = 1): boolean {
    if (!code || code.length !== 6 || !/^\\d{6}$/.test(code)) {
      return false;
    }

    const epochTime = Math.floor(Date.now() / 1000);
    const stepSeconds = 30;
    const currentStep = Math.floor(epochTime / stepSeconds);

    for (let stepOffset = -windowSteps; stepOffset <= windowSteps; stepOffset++) {
      const step = currentStep + stepOffset;
      const expectedCode = this.generateTotpForStep(secret, step);
      if (expectedCode === code) {
        return true;
      }
    }

    return false;
  }

  private static generateTotpForStep(secret: string, step: number): string {
    const buffer = Buffer.alloc(8);
    buffer.writeBigInt64BE(BigInt(step));
    const hmac = createHmac('sha1', Buffer.from(secret, 'utf-8'));
    hmac.update(buffer);
    const digest = hmac.digest();

    const offset = digest[digest.length - 1] & 0x0f;
    const binary =
      ((digest[offset] & 0x7f) << 24) |
      ((digest[offset + 1] & 0xff) << 16) |
      ((digest[offset + 2] & 0xff) << 8) |
      (digest[offset + 3] & 0xff);

    const otp = binary % 1000000;
    return otp.toString().padStart(6, '0');
  }
}
""")

    write_file("services/auth-service/src/services/rbac-policy.service.ts", """import { UserRole } from '@novacommerce/core-types';

export enum Permission {
  // Products & Catalog
  PRODUCT_READ = 'product:read',
  PRODUCT_CREATE = 'product:create',
  PRODUCT_UPDATE = 'product:update',
  PRODUCT_DELETE = 'product:delete',

  // Orders
  ORDER_READ_OWN = 'order:read_own',
  ORDER_READ_ALL = 'order:read_all',
  ORDER_CREATE = 'order:create',
  ORDER_CANCEL = 'order:cancel',
  ORDER_REFUND = 'order:refund',

  // Inventory
  INVENTORY_READ = 'inventory:read',
  INVENTORY_ADJUST = 'inventory:adjust',
  INVENTORY_TRANSFER = 'inventory:transfer',

  // Payments & Ledger
  PAYMENT_PROCESS = 'payment:process',
  LEDGER_VIEW = 'ledger:view',
  LEDGER_EXPORT = 'ledger:export',

  // Users & IAM
  USER_READ_OWN = 'user:read_own',
  USER_READ_ALL = 'user:read_all',
  USER_MANAGE_ROLES = 'user:manage_roles',
  AUDIT_LOG_VIEW = 'audit:view'
}

export const ROLE_PERMISSION_MATRIX: Record<UserRole, Permission[]> = {
  [UserRole.SUPER_ADMIN]: Object.values(Permission),
  [UserRole.ADMIN]: [
    Permission.PRODUCT_READ, Permission.PRODUCT_CREATE, Permission.PRODUCT_UPDATE, Permission.PRODUCT_DELETE,
    Permission.ORDER_READ_ALL, Permission.ORDER_CREATE, Permission.ORDER_CANCEL, Permission.ORDER_REFUND,
    Permission.INVENTORY_READ, Permission.INVENTORY_ADJUST, Permission.INVENTORY_TRANSFER,
    Permission.PAYMENT_PROCESS, Permission.LEDGER_VIEW, Permission.LEDGER_EXPORT,
    Permission.USER_READ_ALL, Permission.USER_MANAGE_ROLES, Permission.AUDIT_LOG_VIEW
  ],
  [UserRole.OPERATIONS_MANAGER]: [
    Permission.PRODUCT_READ, Permission.PRODUCT_UPDATE,
    Permission.ORDER_READ_ALL, Permission.ORDER_CANCEL,
    Permission.INVENTORY_READ, Permission.INVENTORY_ADJUST, Permission.INVENTORY_TRANSFER
  ],
  [UserRole.INVENTORY_MANAGER]: [
    Permission.PRODUCT_READ,
    Permission.INVENTORY_READ, Permission.INVENTORY_ADJUST, Permission.INVENTORY_TRANSFER
  ],
  [UserRole.FINANCE_ANALYST]: [
    Permission.ORDER_READ_ALL,
    Permission.LEDGER_VIEW, Permission.LEDGER_EXPORT,
    Permission.PAYMENT_PROCESS, Permission.AUDIT_LOG_VIEW
  ],
  [UserRole.SUPPORT_AGENT]: [
    Permission.PRODUCT_READ,
    Permission.ORDER_READ_ALL, Permission.ORDER_CANCEL,
    Permission.USER_READ_ALL
  ],
  [UserRole.CUSTOMER]: [
    Permission.PRODUCT_READ,
    Permission.ORDER_READ_OWN, Permission.ORDER_CREATE,
    Permission.USER_READ_OWN
  ],
  [UserRole.GUEST]: [
    Permission.PRODUCT_READ
  ],
  [UserRole.SYSTEM_INTERNAL]: Object.values(Permission)
};

export class RbacPolicyEngine {
  public static hasPermission(role: UserRole, permission: Permission): boolean {
    const permissions = ROLE_PERMISSION_MATRIX[role] || [];
    return permissions.includes(permission);
  }

  public static hasAllPermissions(role: UserRole, permissions: Permission[]): boolean {
    return permissions.every(p => this.hasPermission(role, p));
  }

  public static hasAnyPermission(role: UserRole, permissions: Permission[]): boolean {
    return permissions.some(p => this.hasPermission(role, p));
  }
}
""")

    # 2. Catalog Service: Search Indexing
    write_file("services/catalog-service/src/services/search-indexing.service.ts", """import { ProductEntity } from '@novacommerce/core-types';

export interface SearchFilter {
  categoryId?: string;
  minPriceCents?: number;
  maxPriceCents?: number;
  tags?: string[];
  inStockOnly?: boolean;
}

export interface SearchResult {
  product: ProductEntity;
  score: number;
}

export class SearchIndexingService {
  private readonly documents: Map<string, ProductEntity> = new Map();
  private readonly invertedIndex: Map<string, Set<string>> = new Map();

  public indexProduct(product: ProductEntity): void {
    this.documents.set(product.id, product);

    const tokens = this.tokenize(`${product.name} ${product.description} ${product.sku} ${product.tags.join(' ')}`);
    for (const token of tokens) {
      if (!this.invertedIndex.has(token)) {
        this.invertedIndex.set(token, new Set());
      }
      this.invertedIndex.get(token)!.add(product.id);
    }
  }

  public search(query: string, filter?: SearchFilter, limit: number = 20): SearchResult[] {
    const queryTokens = this.tokenize(query);
    const scoreMap: Map<string, number> = new Map();

    for (const token of queryTokens) {
      const matchingDocIds = this.invertedIndex.get(token);
      if (matchingDocIds) {
        for (const docId of matchingDocIds) {
          const currentScore = scoreMap.get(docId) || 0;
          scoreMap.set(docId, currentScore + 1);
        }
      }
    }

    const results: SearchResult[] = [];
    for (const [docId, score] of scoreMap.entries()) {
      const product = this.documents.get(docId);
      if (!product || !product.isActive) continue;

      if (filter?.categoryId && product.categoryId !== filter.categoryId) continue;
      if (filter?.minPriceCents && product.basePrice.amount < filter.minPriceCents) continue;
      if (filter?.maxPriceCents && product.basePrice.amount > filter.maxPriceCents) continue;
      if (filter?.tags && !filter.tags.every(t => product.tags.includes(t))) continue;

      results.push({ product, score });
    }

    results.sort((a, b) => b.score - a.score);
    return results.slice(0, limit);
  }

  private tokenize(text: string): string[] {
    return text
      .toLowerCase()
      .replace(/[^a-z0-9\\s]/g, '')
      .split(/\\s+/)
      .filter(t => t.length > 1);
  }
}
""")

    # 3. Notification Service: Templates
    write_file("services/notification-service/src/templates/template-registry.ts", """export interface EmailTemplateDefinition {
  subject: string;
  htmlBody: string;
  textBody: string;
}

export const TRANSACTIONAL_TEMPLATES: Record<string, (data: any) => EmailTemplateDefinition> = {
  'order_confirmation': (d) => ({
    subject: `Order Confirmation #${d.orderNumber} - NovaCommerce`,
    htmlBody: `<h1>Thank you for your order!</h1><p>Your order <strong>#${d.orderNumber}</strong> totaling <strong>$${(d.totalAmount / 100).toFixed(2)}</strong> has been confirmed and is being processed.</p>`,
    textBody: `Thank you for your order #${d.orderNumber} totaling $${(d.totalAmount / 100).toFixed(2)}.`
  }),
  'shipping_dispatched': (d) => ({
    subject: `Your order #${d.orderNumber} has shipped!`,
    htmlBody: `<h1>Your shipment is on the way!</h1><p>Tracking number: <a href="${d.trackingUrl}">${d.trackingNumber}</a> via ${d.carrier}.</p>`,
    textBody: `Your order #${d.orderNumber} has shipped. Tracking: ${d.trackingNumber} via ${d.carrier}.`
  }),
  'payment_receipt': (d) => ({
    subject: `Receipt for Payment #${d.transactionReference}`,
    htmlBody: `<h1>Payment Received</h1><p>We received your payment of <strong>$${(d.amount / 100).toFixed(2)}</strong> via ${d.methodType}.</p>`,
    textBody: `Payment of $${(d.amount / 100).toFixed(2)} received for transaction ${d.transactionReference}.`
  }),
  'password_reset': (d) => ({
    subject: 'Reset Your NovaCommerce Password',
    htmlBody: `<h1>Password Reset</h1><p>Click <a href="${d.resetUrl}">here</a> to reset your password. Link expires in 15 minutes.</p>`,
    textBody: `Reset your password by opening: ${d.resetUrl}`
  }),
  'mfa_alert': (d) => ({
    subject: 'Security Alert: Two-Factor Authentication Updated',
    htmlBody: `<h1>Security Notice</h1><p>MFA was modified on your account at ${new Date().toISOString()} from IP ${d.ipAddress}.</p>`,
    textBody: `MFA was modified on your account from IP ${d.ipAddress}.`
  })
};
""")

    # 4. Deep Unit Test Suites
    write_file("services/auth-service/tests/mfa.test.ts", """import { MfaService } from '../src/services/mfa.service.js';

describe('MFA TOTP Suite', () => {
  it('should generate valid secret and backup codes', () => {
    const setup = MfaService.generateSecret('user@novacommerce.io');
    expect(setup.secret.length).toBeGreaterThanOrEqual(16);
    expect(setup.otpauthUrl).toContain('otpauth://totp/');
    expect(setup.backupCodes.length).toBe(8);
  });
});
""")

    write_file("services/auth-service/tests/rbac.test.ts", """import { RbacPolicyEngine, Permission } from '../src/services/rbac-policy.service.js';
import { UserRole } from '@novacommerce/core-types';

describe('RBAC Policy Suite', () => {
  it('should grant SUPER_ADMIN all permissions', () => {
    expect(RbacPolicyEngine.hasPermission(UserRole.SUPER_ADMIN, Permission.PRODUCT_DELETE)).toBe(true);
    expect(RbacPolicyEngine.hasPermission(UserRole.SUPER_ADMIN, Permission.LEDGER_VIEW)).toBe(true);
  });

  it('should restrict CUSTOMER to own resources only', () => {
    expect(RbacPolicyEngine.hasPermission(UserRole.CUSTOMER, Permission.PRODUCT_READ)).toBe(true);
    expect(RbacPolicyEngine.hasPermission(UserRole.CUSTOMER, Permission.PRODUCT_DELETE)).toBe(false);
    expect(RbacPolicyEngine.hasPermission(UserRole.CUSTOMER, Permission.LEDGER_VIEW)).toBe(false);
  });
});
""")

    write_file("services/catalog-service/tests/search.test.ts", """import { SearchIndexingService } from '../src/services/search-indexing.service.js';
import { Currency } from '@novacommerce/core-types';

describe('Search Indexing Suite', () => {
  const searchIndex = new SearchIndexingService();

  beforeAll(() => {
    searchIndex.indexProduct({
      id: 'p1',
      sku: 'NOVA-HEADPHONE-01',
      name: 'Wireless Noise Canceling Headphones Pro',
      slug: 'wireless-nc-headphones',
      description: 'Superior sound quality with active noise cancellation and 40h battery.',
      categoryId: 'cat_audio',
      basePrice: { amount: 29900, currency: Currency.USD },
      isActive: true,
      tags: ['audio', 'wireless', 'bluetooth'],
      attributes: {},
      images: [],
      createdAt: new Date(),
      updatedAt: new Date()
    });
  });

  it('should find indexed product by token match', () => {
    const results = searchIndex.search('Noise Canceling');
    expect(results.length).toBe(1);
    expect(results[0].product.sku).toBe('NOVA-HEADPHONE-01');
  });

  it('should filter search results by price range', () => {
    const results = searchIndex.search('Headphones', { minPriceCents: 50000 });
    expect(results.length).toBe(0);
  });
});
""")

    write_file("services/order-service/tests/discounts.test.ts", """import { PromotionEngine, DiscountType } from '../src/domain/promotions-engine.js';

describe('Promotions & Discounts Suite', () => {
  const engine = new PromotionEngine();

  beforeAll(() => {
    engine.registerCoupon({
      code: 'SAVE20',
      type: DiscountType.PERCENTAGE,
      value: 20,
      minimumCartAmountCents: 5000,
      maxUsageLimit: 1000,
      currentUsageCount: 0,
      validFrom: new Date(Date.now() - 86400000),
      validUntil: new Date(Date.now() + 86400000),
      isActive: true
    });
  });

  it('should apply 20% discount on valid subtotal', () => {
    const result = engine.evaluateCoupon('SAVE20', [{ sku: 'SKU-1', categoryId: 'c1', unitPriceCents: 10000, quantity: 1 }], 10000);
    expect(result.discountAmountCents).toBe(2000);
  });

  it('should reject coupon if minimum subtotal not met', () => {
    expect(() => {
      engine.evaluateCoupon('SAVE20', [{ sku: 'SKU-1', categoryId: 'c1', unitPriceCents: 2000, quantity: 1 }], 2000);
    }).toThrow(/requires a minimum cart subtotal/);
  });
});
""")

    write_file("services/fulfillment-service/tests/bin-packing.test.ts", """import { BinPackingOptimizer } from '../src/domain/bin-packing.js';

describe('3D Bin Packing & Box Selection Suite', () => {
  it('should select appropriate shipper box based on items volume and weight', () => {
    const plan = BinPackingOptimizer.optimizePackage([
      { sku: 'ITEM-1', quantity: 2, weightGrams: 400, dimensionsMm: { length: 150, width: 100, height: 50 } }
    ]);

    expect(plan.selectedBox).toBeDefined();
    expect(plan.billableWeightGrams).toBeGreaterThan(800);
    expect(plan.volumeUtilizationPercent).toBeGreaterThan(0);
  });
});
""")

    print("Generated deep services and comprehensive unit tests.")

if __name__ == "__main__":
    generate_deep_services_and_tests()
