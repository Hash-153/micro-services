import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def build_order_domain():
    print("Generating Order domain...")
    
    # 1. State Machine
    write_file("services/order-service/src/domain/order-lifecycle.ts", """import { OrderStatus } from '@novacommerce/core-types';

export class OrderLifecycleStateMachine {
  private static readonly VALID_TRANSITIONS: Record<OrderStatus, OrderStatus[]> = {
    [OrderStatus.DRAFT]: [OrderStatus.PENDING_PAYMENT, OrderStatus.CANCELLED],
    [OrderStatus.PENDING_PAYMENT]: [OrderStatus.PAYMENT_AUTHORIZED, OrderStatus.PAYMENT_FAILED, OrderStatus.CANCELLED, OrderStatus.EXPIRED],
    [OrderStatus.PAYMENT_AUTHORIZED]: [OrderStatus.PROCESSING, OrderStatus.INVENTORY_RESERVED, OrderStatus.CANCELLED],
    [OrderStatus.PAYMENT_FAILED]: [OrderStatus.PENDING_PAYMENT, OrderStatus.CANCELLED, OrderStatus.EXPIRED],
    [OrderStatus.PROCESSING]: [OrderStatus.INVENTORY_RESERVED, OrderStatus.INVENTORY_ALLOCATION_FAILED, OrderStatus.CANCELLED],
    [OrderStatus.INVENTORY_RESERVED]: [OrderStatus.PACKED, OrderStatus.CANCELLED],
    [OrderStatus.INVENTORY_ALLOCATION_FAILED]: [OrderStatus.CANCELLED, OrderStatus.PROCESSING],
    [OrderStatus.PACKED]: [OrderStatus.DISPATCHED, OrderStatus.CANCELLED],
    [OrderStatus.DISPATCHED]: [OrderStatus.IN_TRANSIT, OrderStatus.DELIVERED, OrderStatus.RETURNED_TO_SENDER],
    [OrderStatus.IN_TRANSIT]: [OrderStatus.OUT_FOR_DELIVERY, OrderStatus.DELIVERED, OrderStatus.FAILED_ATTEMPT, OrderStatus.LOST_IN_TRANSIT],
    [OrderStatus.OUT_FOR_DELIVERY]: [OrderStatus.DELIVERED, OrderStatus.FAILED_ATTEMPT],
    [OrderStatus.DELIVERED]: [OrderStatus.REFUND_REQUESTED, OrderStatus.REFUNDED, OrderStatus.PARTIALLY_REFUNDED],
    [OrderStatus.CANCELLED]: [],
    [OrderStatus.REFUND_REQUESTED]: [OrderStatus.REFUNDED, OrderStatus.PARTIALLY_REFUNDED, OrderStatus.DELIVERED],
    [OrderStatus.REFUNDED]: [],
    [OrderStatus.PARTIALLY_REFUNDED]: [OrderStatus.REFUNDED],
    [OrderStatus.EXPIRED]: []
  };

  public static canTransition(current: OrderStatus, next: OrderStatus): boolean {
    const allowed = this.VALID_TRANSITIONS[current];
    return allowed ? allowed.includes(next) : false;
  }

  public static validateTransition(current: OrderStatus, next: OrderStatus): void {
    if (!this.canTransition(current, next)) {
      throw new Error(`Illegal order state transition from ${current} to ${next}`);
    }
  }

  public static isTerminal(status: OrderStatus): boolean {
    return [OrderStatus.CANCELLED, OrderStatus.REFUNDED, OrderStatus.EXPIRED].includes(status);
  }

  public static isCancellable(status: OrderStatus): boolean {
    return [
      OrderStatus.DRAFT,
      OrderStatus.PENDING_PAYMENT,
      OrderStatus.PAYMENT_AUTHORIZED,
      OrderStatus.PROCESSING,
      OrderStatus.INVENTORY_RESERVED,
      OrderStatus.PACKED
    ].includes(status);
  }
}
""")

    # 2. 50-State Tax Engine
    write_file("services/order-service/src/domain/us-tax-engine.ts", """export interface TaxCalculationResult {
  stateCode: string;
  taxableAmountCents: number;
  taxRatePercent: number;
  taxAmountCents: number;
  jurisdiction: string;
  isExempt: boolean;
}

export class USTaxEngine {
  private static readonly STATE_RATES: Record<string, { rate: number; name: string }> = {
    AL: { rate: 4.00, name: 'Alabama' },
    AK: { rate: 0.00, name: 'Alaska' },
    AZ: { rate: 5.60, name: 'Arizona' },
    AR: { rate: 6.50, name: 'Arkansas' },
    CA: { rate: 7.25, name: 'California' },
    CO: { rate: 2.90, name: 'Colorado' },
    CT: { rate: 6.35, name: 'Connecticut' },
    DE: { rate: 0.00, name: 'Delaware' },
    FL: { rate: 6.00, name: 'Florida' },
    GA: { rate: 4.00, name: 'Georgia' },
    HI: { rate: 4.00, name: 'Hawaii' },
    ID: { rate: 6.00, name: 'Idaho' },
    IL: { rate: 6.25, name: 'Illinois' },
    IN: { rate: 7.00, name: 'Indiana' },
    IA: { rate: 6.00, name: 'Iowa' },
    KS: { rate: 6.50, name: 'Kansas' },
    KY: { rate: 6.00, name: 'Kentucky' },
    LA: { rate: 4.45, name: 'Louisiana' },
    ME: { rate: 5.50, name: 'Maine' },
    MD: { rate: 6.00, name: 'Maryland' },
    MA: { rate: 6.25, name: 'Massachusetts' },
    MI: { rate: 6.00, name: 'Michigan' },
    MN: { rate: 6.875, name: 'Minnesota' },
    MS: { rate: 7.00, name: 'Mississippi' },
    MO: { rate: 4.225, name: 'Missouri' },
    MT: { rate: 0.00, name: 'Montana' },
    NE: { rate: 5.50, name: 'Nebraska' },
    NV: { rate: 6.85, name: 'Nevada' },
    NH: { rate: 0.00, name: 'New Hampshire' },
    NJ: { rate: 6.625, name: 'New Jersey' },
    NM: { rate: 5.00, name: 'New Mexico' },
    NY: { rate: 4.00, name: 'New York' },
    NC: { rate: 4.75, name: 'North Carolina' },
    ND: { rate: 5.00, name: 'North Dakota' },
    OH: { rate: 5.75, name: 'Ohio' },
    OK: { rate: 4.50, name: 'Oklahoma' },
    OR: { rate: 0.00, name: 'Oregon' },
    PA: { rate: 6.00, name: 'Pennsylvania' },
    RI: { rate: 7.00, name: 'Rhode Island' },
    SC: { rate: 6.00, name: 'South Carolina' },
    SD: { rate: 4.20, name: 'South Dakota' },
    TN: { rate: 7.00, name: 'Tennessee' },
    TX: { rate: 6.25, name: 'Texas' },
    UT: { rate: 6.10, name: 'Utah' },
    VT: { rate: 6.00, name: 'Vermont' },
    VA: { rate: 5.30, name: 'Virginia' },
    WA: { rate: 6.50, name: 'Washington' },
    WV: { rate: 6.00, name: 'West Virginia' },
    WI: { rate: 5.00, name: 'Wisconsin' },
    WY: { rate: 4.00, name: 'Wyoming' },
    DC: { rate: 6.00, name: 'District of Columbia' }
  };

  public static calculate(amountCents: number, stateCode: string): TaxCalculationResult {
    const normalized = stateCode.toUpperCase().trim();
    const config = this.STATE_RATES[normalized];

    if (!config) {
      // Default to zero tax for unrecognized international jurisdiction
      return {
        stateCode: normalized,
        taxableAmountCents: amountCents,
        taxRatePercent: 0.0,
        taxAmountCents: 0,
        jurisdiction: 'Default Jurisdiction',
        isExempt: true
      };
    }

    const taxAmountCents = Math.round((amountCents * config.rate) / 100);
    return {
      stateCode: normalized,
      taxableAmountCents: amountCents,
      taxRatePercent: config.rate,
      taxAmountCents,
      jurisdiction: config.name,
      isExempt: config.rate === 0.0
    };
  }
}
""")

    # 3. Promotions & Discount Engine
    write_file("services/order-service/src/domain/promotions-engine.ts", """export interface CouponRule {
  code: string;
  discountType: 'PERCENTAGE' | 'FIXED_AMOUNT' | 'FREE_SHIPPING';
  discountValue: number; // e.g. 15 for 15% or 1000 for $10.00
  minimumOrderValueCents: number;
  maximumDiscountCents?: number;
  validFrom: Date;
  validUntil: Date;
  usageLimit: number;
  currentUsageCount: number;
  applicableSkus?: string[];
  isActive: boolean;
}

export interface DiscountResult {
  couponCode: string;
  discountAmountCents: number;
  isShippingFree: boolean;
  message: string;
}

export class PromotionsEngine {
  private rules: Map<string, CouponRule> = new Map();

  constructor() {
    this.registerDefaultCoupons();
  }

  private registerDefaultCoupons(): void {
    this.registerCoupon({
      code: 'WELCOME10',
      discountType: 'PERCENTAGE',
      discountValue: 10,
      minimumOrderValueCents: 2000,
      validFrom: new Date('2026-01-01'),
      validUntil: new Date('2026-12-31'),
      usageLimit: 100000,
      currentUsageCount: 420,
      isActive: true
    });

    this.registerCoupon({
      code: 'SUMMERSALE25',
      discountType: 'PERCENTAGE',
      discountValue: 25,
      minimumOrderValueCents: 5000,
      maximumDiscountCents: 5000,
      validFrom: new Date('2026-06-01'),
      validUntil: new Date('2026-09-30'),
      usageLimit: 50000,
      currentUsageCount: 1520,
      isActive: true
    });

    this.registerCoupon({
      code: 'FREESHIP',
      discountType: 'FREE_SHIPPING',
      discountValue: 0,
      minimumOrderValueCents: 3500,
      validFrom: new Date('2026-01-01'),
      validUntil: new Date('2026-12-31'),
      usageLimit: 200000,
      currentUsageCount: 8900,
      isActive: true
    });
  }

  public registerCoupon(rule: CouponRule): void {
    this.rules.set(rule.code.toUpperCase().trim(), rule);
  }

  public applyCoupon(code: string, subtotalCents: number, shippingFeeCents: number): DiscountResult {
    const cleanCode = code.toUpperCase().trim();
    const rule = this.rules.get(cleanCode);

    if (!rule) {
      throw new Error(`Invalid promotion code: ${code}`);
    }

    if (!rule.isActive) {
      throw new Error(`Promotion code ${code} is no longer active`);
    }

    const now = new Date();
    if (now < rule.validFrom || now > rule.validUntil) {
      throw new Error(`Promotion code ${code} has expired`);
    }

    if (rule.currentUsageCount >= rule.usageLimit) {
      throw new Error(`Promotion code ${code} usage limit reached`);
    }

    if (subtotalCents < rule.minimumOrderValueCents) {
      throw new Error(`Order minimum of $${(rule.minimumOrderValueCents / 100).toFixed(2)} required for ${code}`);
    }

    let discountCents = 0;
    let isFreeShipping = false;

    if (rule.discountType === 'PERCENTAGE') {
      discountCents = Math.round((subtotalCents * rule.discountValue) / 100);
      if (rule.maximumDiscountCents && discountCents > rule.maximumDiscountCents) {
        discountCents = rule.maximumDiscountCents;
      }
    } else if (rule.discountType === 'FIXED_AMOUNT') {
      discountCents = Math.min(rule.discountValue, subtotalCents);
    } else if (rule.discountType === 'FREE_SHIPPING') {
      isFreeShipping = true;
      discountCents = shippingFeeCents;
    }

    rule.currentUsageCount++;

    return {
      couponCode: cleanCode,
      discountAmountCents: discountCents,
      isShippingFree: isFreeShipping,
      message: `Coupon ${cleanCode} applied successfully.`
    };
  }
}
""")

    # 4. Invoice HTML Generator
    write_file("services/order-service/src/domain/invoice-builder.ts", """import { OrderEntity } from '@novacommerce/core-types';

export class InvoiceBuilder {
  public static generateHtmlInvoice(order: OrderEntity): string {
    const formattedDate = new Date(order.createdAt).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });

    const itemsHtml = order.items.map(item => `
      <tr>
        <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; font-family: monospace;">${item.sku}</td>
        <td style="padding: 12px; border-bottom: 1px solid #e2e8f0;">${item.productName}</td>
        <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: center;">${item.quantity}</td>
        <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: right;">$${(item.unitPrice.amount / 100).toFixed(2)}</td>
        <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: right;">$${(item.total.amount / 100).toFixed(2)}</td>
      </tr>
    `).join('');

    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Commercial Invoice #${order.orderNumber}</title>
  <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #1a202c; padding: 40px; }
    .header { display: flex; justify-content: space-between; border-bottom: 2px solid #2b6cb0; padding-bottom: 20px; }
    .company { font-size: 24px; font-weight: bold; color: #2b6cb0; }
    .invoice-details { text-align: right; }
    .addresses { display: flex; justify-content: space-between; margin-top: 30px; }
    .box { width: 45%; background: #f7fafc; padding: 15px; border-radius: 6px; }
    table { width: 100%; border-collapse: collapse; margin-top: 30px; }
    th { background: #edf2f7; padding: 12px; text-align: left; font-size: 12px; text-transform: uppercase; }
    .summary { margin-top: 30px; display: flex; justify-content: flex-end; }
    .summary-table { width: 300px; }
    .summary-table td { padding: 8px; }
    .total-row { font-size: 18px; font-weight: bold; color: #2b6cb0; border-top: 2px solid #2b6cb0; }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="company">NovaCommerce Technologies</div>
      <div>Enterprise Logistics & Commerce Solutions</div>
      <div>100 Market St, San Francisco, CA 94105</div>
      <div>support@novacommerce.io</div>
    </div>
    <div class="invoice-details">
      <h2>COMMERCIAL INVOICE</h2>
      <div><strong>Invoice #:</strong> ${order.orderNumber}</div>
      <div><strong>Date:</strong> ${formattedDate}</div>
      <div><strong>Status:</strong> ${order.status}</div>
      <div><strong>Payment Ref:</strong> ${order.paymentId || 'N/A'}</div>
    </div>
  </div>

  <div class="addresses">
    <div class="box">
      <strong>Billed To:</strong><br>
      ${order.billingAddress.recipientName}<br>
      ${order.billingAddress.streetLine1}<br>
      ${order.billingAddress.city}, ${order.billingAddress.stateOrProvince} ${order.billingAddress.postalCode}<br>
      ${order.billingAddress.countryCode}
    </div>
    <div class="box">
      <strong>Shipped To:</strong><br>
      ${order.shippingAddress.recipientName}<br>
      ${order.shippingAddress.streetLine1}<br>
      ${order.shippingAddress.city}, ${order.shippingAddress.stateOrProvince} ${order.shippingAddress.postalCode}<br>
      ${order.shippingAddress.countryCode}
    </div>
  </div>

  <table>
    <thead>
      <tr>
        <th>SKU</th>
        <th>Product Description</th>
        <th style="text-align: center;">Qty</th>
        <th style="text-align: right;">Unit Price</th>
        <th style="text-align: right;">Total</th>
      </tr>
    </thead>
    <tbody>
      ${itemsHtml}
    </tbody>
  </table>

  <div class="summary">
    <table class="summary-table">
      <tr>
        <td>Subtotal:</td>
        <td style="text-align: right;">$${(order.subtotalAmount.amount / 100).toFixed(2)}</td>
      </tr>
      <tr>
        <td>Sales Tax:</td>
        <td style="text-align: right;">$${(order.taxAmount.amount / 100).toFixed(2)}</td>
      </tr>
      <tr>
        <td>Shipping & Freight:</td>
        <td style="text-align: right;">$${(order.shippingFeeAmount.amount / 100).toFixed(2)}</td>
      </tr>
      <tr>
        <td>Promotions & Discounts:</td>
        <td style="text-align: right; color: #e53e3e;">-$${(order.discountAmount.amount / 100).toFixed(2)}</td>
      </tr>
      <tr class="total-row">
        <td>Total Due:</td>
        <td style="text-align: right;">$${(order.totalAmount.amount / 100).toFixed(2)} ${order.totalAmount.currency}</td>
      </tr>
    </table>
  </div>
</body>
</html>`;
  }
}
""")

if __name__ == "__main__":
    build_order_domain()
