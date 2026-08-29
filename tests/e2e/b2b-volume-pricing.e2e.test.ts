import { PricingTierService } from '../../services/catalog-service/src/domain/pricing-tier.js';
import { Currency } from '@novacommerce/core-types';

describe('E2E Scenario: B2B Volume Pricing Matrix & Tiered Quantity Discounts', () => {
  it('should apply tier discounts accurately across quantity bands', () => {
    const basePrice = { amount: 10000, currency: Currency.USD }; // $100.00 base

    // 1 item (Standard Retail: Tier 1 -> 0% discount)
    const price1 = PricingTierService.calculatePrice(basePrice, 1);
    expect(price1.finalUnitPrice.amount).toBe(10000);
    expect(price1.totalAmount.amount).toBe(10000);
    expect(price1.discountPercentApplied).toBe(0);

    // 15 items (Wholesale: Tier 2 -> 10% discount)
    const price15 = PricingTierService.calculatePrice(basePrice, 15);
    expect(price15.finalUnitPrice.amount).toBe(9000);
    expect(price15.totalAmount.amount).toBe(135000);
    expect(price15.discountPercentApplied).toBe(10);

    // 60 items (Distributor: Tier 3 -> 20% discount)
    const price60 = PricingTierService.calculatePrice(basePrice, 60);
    expect(price60.finalUnitPrice.amount).toBe(8000);
    expect(price60.totalAmount.amount).toBe(480000);
    expect(price60.discountPercentApplied).toBe(20);

    // 250 items (Enterprise Partner: Tier 4 -> 30% discount)
    const price250 = PricingTierService.calculatePrice(basePrice, 250);
    expect(price250.finalUnitPrice.amount).toBe(7000);
    expect(price250.totalAmount.amount).toBe(1750000);
    expect(price250.discountPercentApplied).toBe(30);
  });
});
