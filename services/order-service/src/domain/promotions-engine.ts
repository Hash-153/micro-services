export interface CouponRule {
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
