import { PromotionEngine, DiscountType } from '../src/domain/promotions-engine.js';

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
