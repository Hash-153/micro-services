import { CouponRule, DiscountResult } from './promotions-engine.js';

export interface StackingEvaluationResult {
  appliedCoupons: DiscountResult[];
  totalDiscountAmountCents: number;
  isShippingFree: boolean;
  rejectedCoupons: { code: string; reason: string }[];
}

export class CouponStackingEngine {
  public static evaluateStack(
    coupons: CouponRule[],
    subtotalCents: number,
    shippingFeeCents: number
  ): StackingEvaluationResult {
    const applied: DiscountResult[] = [];
    const rejected: { code: string; reason: string }[] = [];
    let currentSubtotal = subtotalCents;
    let totalDiscount = 0;
    let freeShipping = false;

    // Sort by discount magnitude descending
    const sorted = [...coupons].sort((a, b) => b.discountValue - a.discountValue);

    for (const coupon of sorted) {
      if (coupon.discountType === 'FREE_SHIPPING') {
        if (!freeShipping) {
          freeShipping = true;
          applied.push({
            couponCode: coupon.code,
            discountAmountCents: shippingFeeCents,
            isShippingFree: true,
            message: `Free shipping applied via ${coupon.code}`
          });
        } else {
          rejected.push({ code: coupon.code, reason: 'Free shipping already granted by another coupon' });
        }
        continue;
      }

      if (currentSubtotal <= 0) {
        rejected.push({ code: coupon.code, reason: 'Subtotal reduced to $0.00' });
        continue;
      }

      if (currentSubtotal < coupon.minimumOrderValueCents) {
        rejected.push({ code: coupon.code, reason: `Minimum order value $${(coupon.minimumOrderValueCents / 100).toFixed(2)} not met` });
        continue;
      }

      let discount = 0;
      if (coupon.discountType === 'PERCENTAGE') {
        discount = Math.round((currentSubtotal * coupon.discountValue) / 100);
        if (coupon.maximumDiscountCents && discount > coupon.maximumDiscountCents) {
          discount = coupon.maximumDiscountCents;
        }
      } else if (coupon.discountType === 'FIXED_AMOUNT') {
        discount = Math.min(coupon.discountValue, currentSubtotal);
      }

      totalDiscount += discount;
      currentSubtotal -= discount;

      applied.push({
        couponCode: coupon.code,
        discountAmountCents: discount,
        isShippingFree: false,
        message: `Applied ${coupon.code} (-$${(discount / 100).toFixed(2)})`
      });
    }

    return {
      appliedCoupons: applied,
      totalDiscountAmountCents: totalDiscount,
      isShippingFree: freeShipping,
      rejectedCoupons: rejected
    };
  }
}
