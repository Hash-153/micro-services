import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_core_events_schemas():
    pkg_dir = "packages/core-events/src/schemas"
    
    events = [
        ("AuthUserRegisteredEvent", "auth.user.registered", "User", "userId: string; email: string; role: string; firstName: string; lastName: string; phoneNumber?: string;"),
        ("AuthUserLoggedInEvent", "auth.user.logged_in", "User", "userId: string; email: string; ipAddress?: string; userAgent?: string;"),
        ("AuthPasswordResetRequestedEvent", "auth.password.reset_requested", "User", "userId: string; email: string; resetToken: string; expiresAt: Date;"),
        ("AuthMfaEnabledEvent", "auth.mfa.enabled", "User", "userId: string; email: string; enabledAt: Date;"),
        ("UserProfileUpdatedEvent", "user.profile.updated", "UserProfile", "userId: string; firstName: string; lastName: string; timeZone: string; locale: string;"),
        ("UserAddressAddedEvent", "user.address.added", "Address", "addressId: string; userId: string; countryCode: string; postalCode: string; isDefaultShipping: boolean;"),
        ("UserKycVerifiedEvent", "user.kyc.verified", "User", "userId: string; verificationLevel: string; verifiedAt: Date; reviewerId: string;"),
        ("CatalogProductCreatedEvent", "catalog.product.created", "Product", "productId: string; sku: string; name: string; categoryId: string; basePriceCents: number; currency: string;"),
        ("CatalogProductUpdatedEvent", "catalog.product.updated", "Product", "productId: string; sku: string; updatedFields: string[];"),
        ("CatalogPriceChangedEvent", "catalog.price.changed", "Product", "productId: string; sku: string; oldPriceCents: number; newPriceCents: number; currency: string;"),
        ("InventoryStockUpdatedEvent", "inventory.stock.updated", "InventoryStock", "sku: string; warehouseId: string; previousOnHand: number; newOnHand: number;"),
        ("InventoryReservationCreatedEvent", "inventory.reservation.created", "InventoryReservation", "reservationId: string; reservationCode: string; orderId: string; sku: string; quantity: number; expiresAt: Date;"),
        ("InventoryReservationReleasedEvent", "inventory.reservation.released", "InventoryReservation", "reservationId: string; orderId: string; sku: string; quantity: number;"),
        ("InventoryLowStockAlertEvent", "inventory.stock.low_alert", "InventoryStock", "sku: string; warehouseId: string; currentOnHand: number; safetyThreshold: number;"),
        ("OrderCreatedEvent", "order.created", "Order", "orderId: string; orderNumber: string; userId: string; subtotalCents: number; taxCents: number; totalCents: number; currency: string; itemsCount: number;"),
        ("OrderPaymentPendingEvent", "order.payment_pending", "Order", "orderId: string; orderNumber: string; totalCents: number; currency: string;"),
        ("OrderPaidEvent", "order.paid", "Order", "orderId: string; paymentTransactionId: string; paidAmountCents: number; currency: string;"),
        ("OrderDispatchedEvent", "order.dispatched", "Order", "orderId: string; shipmentId: string; carrier: string; trackingNumber: string;"),
        ("OrderDeliveredEvent", "order.delivered", "Order", "orderId: string; shipmentId: string; deliveredAt: Date; signedBy?: string;"),
        ("OrderCancelledEvent", "order.cancelled", "Order", "orderId: string; reason: string; cancelledBy: string; compensationTriggered: boolean;"),
        ("PaymentAuthorizedEvent", "payment.authorized", "PaymentTransaction", "paymentId: string; orderId: string; amountCents: number; currency: string; provider: string; transactionReference: string;"),
        ("PaymentCapturedEvent", "payment.captured", "PaymentTransaction", "paymentId: string; orderId: string; amountCents: number; currency: string; providerTransactionId: string;"),
        ("PaymentRefundedEvent", "payment.refunded", "PaymentTransaction", "refundId: string; originalPaymentId: string; orderId: string; refundAmountCents: number; currency: string; reason: string;"),
        ("LedgerJournalEntryRecordedEvent", "payment.ledger.recorded", "LedgerJournalEntry", "journalEntryId: string; entryNumber: string; totalAmountCents: number; linesCount: number; postedAt: Date;"),
        ("FulfillmentLabelGeneratedEvent", "fulfillment.label_generated", "Shipment", "shipmentId: string; orderId: string; carrier: string; trackingNumber: string; labelUrl: string;"),
        ("NotificationDispatchedEvent", "notification.sent", "NotificationLog", "notificationId: string; recipient: string; channel: string; templateId: string; dispatchedAt: Date;"),
        ("AnalyticsEventIngestedEvent", "analytics.event.ingested", "AnalyticsEvent", "eventId: string; eventName: string; userId?: string; sessionId?: string; timestamp: Date;")
    ]

    for class_name, event_type, agg_type, fields in events:
        write_file(f"{pkg_dir}/{class_name}.ts", f"""import {{ DomainEvent, EventType }} from '@novacommerce/core-types';

export interface {class_name}Payload {{
  {fields}
}}

export type {class_name} = DomainEvent<{class_name}Payload>;

export class {class_name}Factory {{
  public static create(
    aggregateId: string,
    payload: {class_name}Payload,
    producer: string,
    correlationId?: string
  ): {class_name} {{
    return {{
      id: crypto.randomUUID(),
      eventType: '{event_type}' as EventType,
      aggregateId,
      aggregateType: '{agg_type}',
      version: 1,
      timestamp: new Date().toISOString(),
      correlationId: correlationId || crypto.randomUUID(),
      producer,
      payload
    }};
  }}
}}
""")

    print("Generated Event Schema Factories in core-events.")

def generate_enterprise_services():
    # 1. Auth Service: Session Service & OAuth2 Provider
    write_file("services/auth-service/src/services/session.service.ts", """import { ILogger } from '@novacommerce/core-logger';
import { randomUUID, createHash } from 'crypto';

export interface UserSession {
  sessionId: string;
  userId: string;
  email: string;
  ipAddress: string;
  userAgent: string;
  refreshTokenHash: string;
  isRevoked: boolean;
  expiresAt: Date;
  createdAt: Date;
  lastActivityAt: Date;
}

export class SessionService {
  private readonly sessions: Map<string, UserSession> = new Map();
  private readonly logger: ILogger;

  constructor(logger: ILogger) {
    this.logger = logger.child({ component: 'SessionService' });
  }

  public async createSession(
    userId: string,
    email: string,
    refreshToken: string,
    ipAddress: string = '127.0.0.1',
    userAgent: string = 'Unknown',
    ttlDays: number = 7
  ): Promise<UserSession> {
    const sessionId = randomUUID();
    const refreshTokenHash = createHash('sha256').update(refreshToken).digest('hex');
    const expiresAt = new Date(Date.now() + ttlDays * 24 * 60 * 60 * 1000);

    const session: UserSession = {
      sessionId,
      userId,
      email,
      ipAddress,
      userAgent,
      refreshTokenHash,
      isRevoked: false,
      expiresAt,
      createdAt: new Date(),
      lastActivityAt: new Date()
    };

    this.sessions.set(sessionId, session);
    this.logger.info(`Session created: ${sessionId} for user ${userId}`);
    return session;
  }

  public async getActiveSession(sessionId: string): Promise<UserSession | null> {
    const session = this.sessions.get(sessionId);
    if (!session || session.isRevoked || session.expiresAt < new Date()) {
      return null;
    }
    session.lastActivityAt = new Date();
    return session;
  }

  public async revokeSession(sessionId: string): Promise<boolean> {
    const session = this.sessions.get(sessionId);
    if (session) {
      session.isRevoked = true;
      this.logger.info(`Session revoked: ${sessionId}`);
      return true;
    }
    return false;
  }

  public async revokeAllUserSessions(userId: string): Promise<number> {
    let count = 0;
    for (const session of this.sessions.values()) {
      if (session.userId === userId && !session.isRevoked) {
        session.isRevoked = true;
        count++;
      }
    }
    this.logger.info(`Revoked ${count} sessions for user ${userId}`);
    return count;
  }
}
""")

    # 2. User Service: Organization & Multi-Tenancy
    write_file("services/user-service/src/services/organization.service.ts", """import { ILogger } from '@novacommerce/core-logger';
import { randomUUID } from 'crypto';

export interface OrganizationEntity {
  id: string;
  name: string;
  slug: string;
  billingEmail: string;
  tier: 'FREE' | 'PRO' | 'ENTERPRISE';
  maxSeats: number;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface OrganizationMember {
  id: string;
  organizationId: string;
  userId: string;
  role: 'OWNER' | 'ADMIN' | 'MEMBER' | 'BILLING';
  joinedAt: Date;
}

export class OrganizationService {
  private readonly orgs: Map<string, OrganizationEntity> = new Map();
  private readonly members: Map<string, OrganizationMember[]> = new Map();
  private readonly logger: ILogger;

  constructor(logger: ILogger) {
    this.logger = logger.child({ component: 'OrganizationService' });
  }

  public async createOrganization(name: string, ownerUserId: string, billingEmail: string): Promise<OrganizationEntity> {
    const orgId = randomUUID();
    const slug = name.toLowerCase().replace(/[^a-z0-9]/g, '-');
    const org: OrganizationEntity = {
      id: orgId,
      name,
      slug,
      billingEmail,
      tier: 'PRO',
      maxSeats: 25,
      isActive: true,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.orgs.set(orgId, org);

    const ownerMember: OrganizationMember = {
      id: randomUUID(),
      organizationId: orgId,
      userId: ownerUserId,
      role: 'OWNER',
      joinedAt: new Date()
    };

    this.members.set(orgId, [ownerMember]);
    this.logger.info(`Created Organization '${name}' (${orgId}) for owner ${ownerUserId}`);
    return org;
  }

  public async addMember(orgId: string, userId: string, role: 'ADMIN' | 'MEMBER' | 'BILLING' = 'MEMBER'): Promise<OrganizationMember> {
    const org = this.orgs.get(orgId);
    if (!org) throw new Error(`Organization ${orgId} not found.`);

    const currentMembers = this.members.get(orgId) || [];
    if (currentMembers.length >= org.maxSeats) {
      throw new Error(`Organization seat limit reached (${org.maxSeats}).`);
    }

    const member: OrganizationMember = {
      id: randomUUID(),
      organizationId: orgId,
      userId,
      role,
      joinedAt: new Date()
    };

    currentMembers.push(member);
    this.members.set(orgId, currentMembers);
    return member;
  }

  public async getOrgMembers(orgId: string): Promise<OrganizationMember[]> {
    return this.members.get(orgId) || [];
  }
}
""")

    # 3. Catalog Service: Pricing Tier & B2B Volume Matrix
    write_file("services/catalog-service/src/services/pricing-tier.service.ts", """import { Money, Currency } from '@novacommerce/core-types';

export interface VolumePriceTier {
  minQuantity: number;
  maxQuantity: number | null; // null represents infinity
  unitPriceCents: number;
  discountPercentage: number;
}

export interface CustomerTierPricingRule {
  tierName: 'RETAIL' | 'SILVER' | 'GOLD' | 'PLATINUM' | 'WHOLESALE';
  sku: string;
  volumeTiers: VolumePriceTier[];
}

export class PricingTierService {
  private readonly rules: Map<string, CustomerTierPricingRule[]> = new Map();

  public registerPricingRule(rule: CustomerTierPricingRule): void {
    const list = this.rules.get(rule.sku) || [];
    list.push(rule);
    this.rules.set(rule.sku, list);
  }

  public calculateUnitPrice(
    sku: string,
    quantity: number,
    customerTier: 'RETAIL' | 'SILVER' | 'GOLD' | 'PLATINUM' | 'WHOLESALE' = 'RETAIL',
    basePriceCents: number = 2999
  ): number {
    const skuRules = this.rules.get(sku) || [];
    const tierRule = skuRules.find(r => r.tierName === customerTier);

    if (!tierRule || tierRule.volumeTiers.length === 0) {
      return basePriceCents;
    }

    for (const volumeTier of tierRule.volumeTiers) {
      const matchMin = quantity >= volumeTier.minQuantity;
      const matchMax = volumeTier.maxQuantity === null || quantity <= volumeTier.maxQuantity;

      if (matchMin && matchMax) {
        return volumeTier.unitPriceCents;
      }
    }

    return basePriceCents;
  }
}
""")

    # 4. Inventory Service: Multi-Warehouse Routing Engine
    write_file("services/inventory-service/src/services/warehouse-routing.service.ts", """export interface WarehouseLocation {
  warehouseId: string;
  code: string;
  name: string;
  latitude: number;
  longitude: number;
  availableStock: number;
}

export interface DeliveryDestination {
  latitude: number;
  longitude: number;
  countryCode: string;
  postalCode: string;
}

export class WarehouseRoutingService {
  // Selects nearest warehouse with adequate stock using Haversine distance
  public static selectOptimalWarehouse(
    destination: DeliveryDestination,
    warehouses: WarehouseLocation[],
    requiredQuantity: number
  ): WarehouseLocation | null {
    const eligible = warehouses.filter(w => w.availableStock >= requiredQuantity);
    if (eligible.length === 0) return null;

    let closestWarehouse: WarehouseLocation | null = null;
    let shortestDistanceKm = Infinity;

    for (const wh of eligible) {
      const dist = this.haversineDistanceKm(
        destination.latitude,
        destination.longitude,
        wh.latitude,
        wh.longitude
      );

      if (dist < shortestDistanceKm) {
        shortestDistanceKm = dist;
        closestWarehouse = wh;
      }
    }

    return closestWarehouse;
  }

  private static haversineDistanceKm(lat1: number, lon1: number, lat2: number, lon2: number): number {
    const R = 6371; // Earth radius in km
    const dLat = this.toRadians(lat2 - lat1);
    const dLon = this.toRadians(lon2 - lon1);
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(this.toRadians(lat1)) * Math.cos(this.toRadians(lat2)) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }

  private static toRadians(deg: number): number {
    return deg * (Math.PI / 180);
  }
}
""")

    # 5. Order Service: Invoice Generator
    write_file("services/order-service/src/services/invoice-generator.service.ts", """import { OrderEntity } from '@novacommerce/core-types';

export class InvoiceGenerator {
  public static generateHtmlInvoice(order: OrderEntity, companyName: string = 'NovaCommerce Inc.'): string {
    const itemRows = order.items
      .map(
        item => `<tr>
        <td>${item.sku}</td>
        <td>${item.productName}</td>
        <td>${item.quantity}</td>
        <td>$${(item.unitPrice.amount / 100).toFixed(2)}</td>
        <td>$${(item.total.amount / 100).toFixed(2)}</td>
      </tr>`
      )
      .join('\\n');

    return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Invoice #${order.orderNumber}</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 40px; color: #333; }
    .header { border-bottom: 2px solid #eee; padding-bottom: 20px; margin-bottom: 30px; }
    .invoice-title { font-size: 28px; font-weight: bold; color: #1a365d; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
    th { background: #f7fafc; }
    .totals { margin-top: 30px; text-align: right; font-size: 16px; }
    .total-due { font-size: 22px; font-weight: bold; color: #2b6cb0; }
  </style>
</head>
<body>
  <div class="header">
    <div class="invoice-title">COMMERCIAL INVOICE</div>
    <p><strong>${companyName}</strong><br>100 Enterprise Way, Suite 400, Wilmington, DE 19801</p>
    <p><strong>Invoice Number:</strong> INV-${order.orderNumber}<br>
       <strong>Order Date:</strong> ${order.createdAt.toISOString()}<br>
       <strong>Customer ID:</strong> ${order.userId}</p>
  </div>

  <table>
    <thead>
      <tr>
        <th>SKU</th>
        <th>Description</th>
        <th>Qty</th>
        <th>Unit Price</th>
        <th>Total Amount</th>
      </tr>
    </thead>
    <tbody>
      ${itemRows}
    </tbody>
  </table>

  <div class="totals">
    <p>Subtotal: $${(order.subtotalAmount.amount / 100).toFixed(2)}</p>
    <p>Tax: $${(order.taxAmount.amount / 100).toFixed(2)}</p>
    <p>Shipping & Handling: $${(order.shippingFeeAmount.amount / 100).toFixed(2)}</p>
    <p class="total-due">Total Amount Paid: $${(order.totalAmount.amount / 100).toFixed(2)} ${order.totalAmount.currency}</p>
  </div>
</body>
</html>`;
  }
}
""")

    # 6. Payment Service: Gateway Router & Reconciliation
    write_file("services/payment-service/src/services/payment-gateway-router.service.ts", """import { PaymentGatewayProvider, Currency } from '@novacommerce/core-types';

export class PaymentGatewayRouter {
  public static selectOptimalGateway(currency: Currency, countryCode: string = 'US', amountCents: number = 0): PaymentGatewayProvider {
    if (currency === Currency.EUR || countryCode === 'DE' || countryCode === 'FR' || countryCode === 'NL') {
      return PaymentGatewayProvider.ADYEN;
    }
    if (currency === Currency.USD || countryCode === 'US' || countryCode === 'CA') {
      return PaymentGatewayProvider.STRIPE;
    }
    return PaymentGatewayProvider.MOCK;
  }
}
""")

    # 7. Analytics Service: Revenue Rollup Service
    write_file("services/analytics-service/src/services/revenue-rollup.service.ts", """export interface DailyRevenueMetric {
  date: string;
  grossMerchandiseVolumeCents: number;
  totalOrders: number;
  averageOrderValueCents: number;
  refundedAmountCents: number;
  netRevenueCents: number;
}

export class RevenueRollupService {
  private readonly dailyMetrics: Map<string, DailyRevenueMetric> = new Map();

  public recordTransaction(dateStr: string, amountCents: number, isRefund: boolean = false): void {
    let metric = this.dailyMetrics.get(dateStr);
    if (!metric) {
      metric = {
        date: dateStr,
        grossMerchandiseVolumeCents: 0,
        totalOrders: 0,
        averageOrderValueCents: 0,
        refundedAmountCents: 0,
        netRevenueCents: 0
      };
    }

    if (isRefund) {
      metric.refundedAmountCents += amountCents;
    } else {
      metric.grossMerchandiseVolumeCents += amountCents;
      metric.totalOrders += 1;
    }

    metric.netRevenueCents = metric.grossMerchandiseVolumeCents - metric.refundedAmountCents;
    metric.averageOrderValueCents = metric.totalOrders > 0 ? Math.round(metric.grossMerchandiseVolumeCents / metric.totalOrders) : 0;

    this.dailyMetrics.set(dateStr, metric);
  }

  public getMetricsForPeriod(startDate: string, endDate: string): DailyRevenueMetric[] {
    return Array.from(this.dailyMetrics.values())
      .filter(m => m.date >= startDate && m.date <= endDate)
      .sort((a, b) => a.date.localeCompare(b.date));
  }
}
""")

    print("Enterprise services generated.")

if __name__ == "__main__":
    generate_core_events_schemas()
    generate_enterprise_services()
    print("Massive scale generation completed successfully.")
