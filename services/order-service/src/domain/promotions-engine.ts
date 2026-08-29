import { Money, Currency } from '@novacommerce/core-types';

export enum DiscountType {
  PERCENTAGE = 'PERCENTAGE',
  FIXED_AMOUNT = 'FIXED_AMOUNT',
  FREE_SHIPPING = 'FREE_SHIPPING',
  BUY_X_GET_Y_FREE = 'BUY_X_GET_Y_FREE',
  TIERED_VOLUME = 'TIERED_VOLUME'
}

export interface CouponRule {
  code: string;
  type: DiscountType;
  value: number; // Percentage (e.g. 15 for 15%) or Fixed Minor Units (e.g. 1000 for $10.00)
  minimumCartAmountCents: number;
  maximumDiscountCents?: number;
  applicableSkuList?: string[];
  applicableCategoryIds?: string[];
  maxUsageLimit: number;
  currentUsageCount: number;
  validFrom: Date;
  validUntil: Date;
  isActive: boolean;
}

export interface CartItemForDiscount {
  sku: string;
  categoryId: string;
  unitPriceCents: number;
  quantity: number;
}

export interface DiscountCalculationResult {
  discountAmountCents: number;
  isFreeShipping: boolean;
  couponCode: string;
  appliedRuleType: DiscountType;
  explanation: string;
}

export class PromotionEngine {
  private readonly coupons: Map<string, CouponRule> = new Map();

  public registerCoupon(rule: CouponRule): void {
    this.coupons.set(rule.code.toUpperCase(), rule);
  }

  public evaluateCoupon(
    code: string,
    cartItems: CartItemForDiscount[],
    subtotalCents: number,
    now: Date = new Date()
  ): DiscountCalculationResult {
    const coupon = this.coupons.get(code.toUpperCase());
    if (!coupon) {
      throw new Error(`Coupon '${code}' is invalid or expired.`);
    }

    if (!coupon.isActive) {
      throw new Error(`Coupon '${code}' is deactivated.`);
    }

    if (now < coupon.validFrom || now > coupon.validUntil) {
      throw new Error(`Coupon '${code}' is outside its valid promotion window.`);
    }

    if (coupon.currentUsageCount >= coupon.maxUsageLimit) {
      throw new Error(`Coupon '${code}' has reached its maximum global redemption limit.`);
    }

    if (subtotalCents < coupon.minimumCartAmountCents) {
      throw new Error(
        `Coupon '${code}' requires a minimum cart subtotal of \$${(coupon.minimumCartAmountCents / 100).toFixed(2)}.`
      );
    }

    let discountCents = 0;
    let isFreeShipping = false;
    let explanation = '';

    switch (coupon.type) {
      case DiscountType.PERCENTAGE: {
        const rawDiscount = Math.round((subtotalCents * coupon.value) / 100);
        discountCents = coupon.maximumDiscountCents ? Math.min(rawDiscount, coupon.maximumDiscountCents) : rawDiscount;
        explanation = `Applied ${coupon.value}% discount (-$${(discountCents / 100).toFixed(2)})`;
        break;
      }
      case DiscountType.FIXED_AMOUNT: {
        discountCents = Math.min(subtotalCents, coupon.value);
        explanation = `Applied flat discount (-$${(discountCents / 100).toFixed(2)})`;
        break;
      }
      case DiscountType.FREE_SHIPPING: {
        isFreeShipping = true;
        explanation = 'Applied 100% free standard ground shipping voucher.';
        break;
      }
      case DiscountType.BUY_X_GET_Y_FREE: {
        // Buy 2 Get 1 Free on matching SKUs
        for (const item of cartItems) {
          if (coupon.applicableSkuList?.includes(item.sku) && item.quantity >= 3) {
            const freeItems = Math.floor(item.quantity / 3);
            const saved = freeItems * item.unitPriceCents;
            discountCents += saved;
          }
        }
        explanation = `Applied Buy 2 Get 1 Free promotion (-$${(discountCents / 100).toFixed(2)})`;
        break;
      }
      case DiscountType.TIERED_VOLUME: {
        const totalItemsCount = cartItems.reduce((acc, i) => acc + i.quantity, 0);
        let tierPercent = 0;
        if (totalItemsCount >= 10) tierPercent = 20;
        else if (totalItemsCount >= 5) tierPercent = 10;

        discountCents = Math.round((subtotalCents * tierPercent) / 100);
        explanation = `Applied volume tier discount of ${tierPercent}% (-$${(discountCents / 100).toFixed(2)})`;
        break;
      }
    }

    return {
      discountAmountCents: discountCents,
      isFreeShipping,
      couponCode: coupon.code,
      appliedRuleType: coupon.type,
      explanation
    };
  }
}
