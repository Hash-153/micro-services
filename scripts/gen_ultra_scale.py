import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_controllers_and_routes():
    # 1. User Service Routes & Controllers
    write_file("services/user-service/src/controllers/user-profile.controller.ts", """import { Request, Response, NextFunction } from 'express';
import { UserProfileService } from '../services/user-profile.service.js';
import { ApiResponse } from '@novacommerce/core-types';

export class UserProfileController {
  private readonly service: UserProfileService;

  constructor(service: UserProfileService) {
    this.service = service;
  }

  public getProfile = async (req: any, res: Response, next: NextFunction) => {
    try {
      const userId = req.user.sub || req.user.id;
      const profile = await this.service.getProfile(userId);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: profile
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };

  public updateProfile = async (req: any, res: Response, next: NextFunction) => {
    try {
      const userId = req.user.sub || req.user.id;
      const updated = await this.service.updateProfile(userId, req.body);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: updated
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };

  public listAddresses = async (req: any, res: Response, next: NextFunction) => {
    try {
      const userId = req.user.sub || req.user.id;
      const addresses = await this.service.getAddresses(userId);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: addresses
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };

  public addAddress = async (req: any, res: Response, next: NextFunction) => {
    try {
      const userId = req.user.sub || req.user.id;
      const address = await this.service.addAddress(userId, req.body);
      const response: ApiResponse = {
        success: true,
        statusCode: 201,
        data: address
      };
      res.status(201).json(response);
    } catch (err) {
      next(err);
    }
  };
}
""")

    # 2. Catalog Service Routes & Controllers
    write_file("services/catalog-service/src/controllers/catalog.controller.ts", """import { Request, Response, NextFunction } from 'express';
import { CatalogService } from '../services/catalog.service.js';
import { ApiResponse } from '@novacommerce/core-types';

export class CatalogController {
  private readonly service: CatalogService;

  constructor(service: CatalogService) {
    this.service = service;
  }

  public listProducts = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const page = parseInt(req.query.page as string || '1', 10);
      const limit = parseInt(req.query.limit as string || '20', 10);
      const offset = (page - 1) * limit;
      const { items, total } = await this.service.listProducts(limit, offset);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: items,
        meta: {
          page,
          limit,
          totalItems: total,
          totalPages: Math.ceil(total / limit)
        }
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };

  public getProduct = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const product = await this.service.getProductById(req.params.id);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: product
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };

  public createProduct = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const correlationId = req.headers['x-correlation-id'] as string;
      const product = await this.service.createProduct(req.body, correlationId);
      const response: ApiResponse = {
        success: true,
        statusCode: 201,
        data: product
      };
      res.status(201).json(response);
    } catch (err) {
      next(err);
    }
  };
}
""")

    # 3. Order Service Controller & Saga Endpoints
    write_file("services/order-service/src/controllers/order.controller.ts", """import { Request, Response, NextFunction } from 'express';
import { OrderService } from '../services/order.service.js';
import { ApiResponse, OrderStatus } from '@novacommerce/core-types';

export class OrderController {
  private readonly service: OrderService;

  constructor(service: OrderService) {
    this.service = service;
  }

  public createOrder = async (req: any, res: Response, next: NextFunction) => {
    try {
      const userId = req.user?.sub || req.body.userId || 'usr-anon';
      const correlationId = req.headers['x-correlation-id'] as string;
      const order = await this.service.createOrder(req.body, userId, correlationId);
      const response: ApiResponse = {
        success: true,
        statusCode: 201,
        data: order
      };
      res.status(201).json(response);
    } catch (err) {
      next(err);
    }
  };

  public getOrder = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const order = await this.service.getOrderById(req.params.id);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: order
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };

  public cancelOrder = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const correlationId = req.headers['x-correlation-id'] as string;
      const order = await this.service.updateOrderStatus(req.params.id, OrderStatus.CANCELLED, correlationId);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: order
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };
}
""")

    # 4. Payment Service Controller
    write_file("services/payment-service/src/controllers/payment.controller.ts", """import { Request, Response, NextFunction } from 'express';
import { PaymentService } from '../services/payment.service.js';
import { ApiResponse, Currency } from '@novacommerce/core-types';

export class PaymentController {
  private readonly service: PaymentService;

  constructor(service: PaymentService) {
    this.service = service;
  }

  public authorize = async (req: any, res: Response, next: NextFunction) => {
    try {
      const { orderId, amountCents, currency } = req.body;
      const userId = req.user?.sub || req.body.userId || 'usr-anon';
      const correlationId = req.headers['x-correlation-id'] as string;
      const payment = await this.service.authorizePayment(orderId, userId, amountCents, currency || Currency.USD, correlationId);
      const response: ApiResponse = {
        success: true,
        statusCode: 201,
        data: payment
      };
      res.status(201).json(response);
    } catch (err) {
      next(err);
    }
  };
}
""")

    # 5. Inventory Service Controller
    write_file("services/inventory-service/src/controllers/inventory.controller.ts", """import { Request, Response, NextFunction } from 'express';
import { InventoryService } from '../services/inventory.service.js';
import { ApiResponse } from '@novacommerce/core-types';

export class InventoryController {
  private readonly service: InventoryService;

  constructor(service: InventoryService) {
    this.service = service;
  }

  public setStock = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { sku, warehouseId, quantity } = req.body;
      const stock = await this.service.setStock(sku, warehouseId || 'WH-MAIN-01', quantity);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: stock
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };

  public reserve = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { orderId, sku, quantity } = req.body;
      const correlationId = req.headers['x-correlation-id'] as string;
      const reservation = await this.service.reserveStock(orderId, sku, quantity, correlationId);
      const response: ApiResponse = {
        success: true,
        statusCode: 201,
        data: reservation
      };
      res.status(201).json(response);
    } catch (err) {
      next(err);
    }
  };

  public release = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { orderId } = req.body;
      const correlationId = req.headers['x-correlation-id'] as string;
      await this.service.releaseReservation(orderId, correlationId);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: { message: `Released reservations for order ${orderId}` }
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };
}
""")

    # 6. Fulfillment Service Controller
    write_file("services/fulfillment-service/src/controllers/fulfillment.controller.ts", """import { Request, Response, NextFunction } from 'express';
import { FulfillmentService } from '../services/fulfillment.service.js';
import { ApiResponse } from '@novacommerce/core-types';

export class FulfillmentController {
  private readonly service: FulfillmentService;

  constructor(service: FulfillmentService) {
    this.service = service;
  }

  public createShipment = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { orderId, destinationAddress, carrier } = req.body;
      const correlationId = req.headers['x-correlation-id'] as string;
      const shipment = await this.service.createShipment(orderId, destinationAddress || {}, carrier, correlationId);
      const response: ApiResponse = {
        success: true,
        statusCode: 201,
        data: shipment
      };
      res.status(201).json(response);
    } catch (err) {
      next(err);
    }
  };
}
""")

    print("Controllers generated.")

def generate_additional_test_suites():
    # Auth Service Tests
    write_file("services/auth-service/tests/session.test.ts", """import { SessionService } from '../src/services/session.service.js';
import { Logger } from '@novacommerce/core-logger';

describe('Auth Session Service Suite', () => {
  const logger = Logger.create('test');
  const service = new SessionService(logger);

  it('should create and retrieve active session', async () => {
    const session = await service.createSession('usr-100', 'usr@test.io', 'tok_refresh_123');
    expect(session.sessionId).toBeDefined();
    expect(session.isRevoked).toBe(false);

    const active = await service.getActiveSession(session.sessionId);
    expect(active).toBeDefined();
    expect(active?.userId).toBe('usr-100');
  });

  it('should revoke session on logout', async () => {
    const session = await service.createSession('usr-200', 'usr2@test.io', 'tok_refresh_456');
    await service.revokeSession(session.sessionId);
    const active = await service.getActiveSession(session.sessionId);
    expect(active).toBeNull();
  });
});
""")

    # User Service Tests
    write_file("services/user-service/tests/organization.test.ts", """import { OrganizationService } from '../src/services/organization.service.js';
import { Logger } from '@novacommerce/core-logger';

describe('Organization Service Suite', () => {
  const logger = Logger.create('test');
  const service = new OrganizationService(logger);

  it('should create organization with owner membership', async () => {
    const org = await service.createOrganization('Acme Corp', 'usr-owner-1', 'billing@acme.com');
    expect(org.id).toBeDefined();
    expect(org.slug).toBe('acme-corp');

    const members = await service.getOrgMembers(org.id);
    expect(members.length).toBe(1);
    expect(members[0].role).toBe('OWNER');
  });
});
""")

    # Catalog Service Tests
    write_file("services/catalog-service/tests/pricing-tier.test.ts", """import { PricingTierService } from '../src/services/pricing-tier.service.js';

describe('Pricing Tier Suite', () => {
  const service = new PricingTierService();

  beforeAll(() => {
    service.registerPricingRule({
      tierName: 'WHOLESALE',
      sku: 'SKU-BULK-01',
      volumeTiers: [
        { minQuantity: 1, maxQuantity: 9, unitPriceCents: 2500, discountPercentage: 0 },
        { minQuantity: 10, maxQuantity: 49, unitPriceCents: 2000, discountPercentage: 20 },
        { minQuantity: 50, maxQuantity: null, unitPriceCents: 1500, discountPercentage: 40 }
      ]
    });
  });

  it('should apply volume discount tiers correctly', () => {
    expect(service.calculateUnitPrice('SKU-BULK-01', 5, 'WHOLESALE')).toBe(2500);
    expect(service.calculateUnitPrice('SKU-BULK-01', 20, 'WHOLESALE')).toBe(2000);
    expect(service.calculateUnitPrice('SKU-BULK-01', 100, 'WHOLESALE')).toBe(1500);
  });
});
""")

    # Payment Service Tests
    write_file("services/payment-service/tests/fraud.test.ts", """import { FraudDetector } from '../src/domain/fraud-detector.js';

describe('Fraud Detection Rule Engine Suite', () => {
  it('should allow low risk transaction with matching countries', () => {
    const res = FraudDetector.evaluateRisk({
      userId: 'u1',
      orderId: 'o1',
      amountCents: 4999,
      currency: 'USD',
      ipAddress: '192.168.1.1',
      cardBin: '411111',
      cardCountry: 'US',
      billingCountry: 'US',
      shippingCountry: 'US',
      deviceFingerprint: 'fp_123',
      accountAgeDays: 120,
      previousOrderCount: 15,
      previousDisputeCount: 0
    });

    expect(res.riskLevel).toBe('LOW');
    expect(res.action).toBe('ALLOW');
  });

  it('should flag critical risk on prior disputes and country mismatch', () => {
    const res = FraudDetector.evaluateRisk({
      userId: 'u2',
      orderId: 'o2',
      amountCents: 600000, // $6,000
      currency: 'USD',
      ipAddress: '203.0.113.1',
      cardBin: '411111',
      cardCountry: 'US',
      billingCountry: 'US',
      shippingCountry: 'RU',
      deviceFingerprint: 'fp_999',
      accountAgeDays: 0,
      previousOrderCount: 0,
      previousDisputeCount: 2
    });

    expect(res.riskLevel).toBe('CRITICAL');
    expect(res.action).toBe('REJECT');
    expect(res.flaggedRules).toContain('RULE_GEO_COUNTRY_MISMATCH');
    expect(res.flaggedRules).toContain('RULE_PRIOR_DISPUTE_HISTORY');
  });
});
""")

    # Analytics Service Tests
    write_file("services/analytics-service/tests/revenue-rollup.test.ts", """import { RevenueRollupService } from '../src/services/revenue-rollup.service.js';

describe('Revenue Rollup Analytics Suite', () => {
  const service = new RevenueRollupService();

  it('should compute daily GMV and net revenue with refunds', () => {
    service.recordTransaction('2026-08-29', 10000);
    service.recordTransaction('2026-08-29', 15000);
    service.recordTransaction('2026-08-29', 5000, true); // refund

    const metrics = service.getMetricsForPeriod('2026-08-01', '2026-08-31');
    expect(metrics.length).toBe(1);
    expect(metrics[0].grossMerchandiseVolumeCents).toBe(25000);
    expect(metrics[0].refundedAmountCents).toBe(5000);
    expect(metrics[0].netRevenueCents).toBe(20000);
    expect(metrics[0].totalOrders).toBe(2);
    expect(metrics[0].averageOrderValueCents).toBe(12500);
  });
});
""")

    print("Generated additional test suites.")

if __name__ == "__main__":
    generate_controllers_and_routes()
    generate_additional_test_suites()
    print("Ultra scale generation completed.")
