import { PricingTierService } from '../src/services/pricing-tier.service.js';

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
