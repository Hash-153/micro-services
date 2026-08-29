import { Money, Currency } from '@novacommerce/core-types';

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
