import { Money, Currency } from '@novacommerce/core-types';

export interface VolumePriceTier {
  minimumQuantity: number;
  discountPercentage: number;
  fixedUnitPriceCents?: number;
}

export class PriceTierEngine {
  public static calculateTieredPrice(
    basePriceCents: number,
    quantity: number,
    tiers: VolumePriceTier[]
  ): { unitPriceCents: number; subtotalCents: number; totalSavingsCents: number; appliedTier?: VolumePriceTier } {
    const sortedTiers = [...tiers].sort((a, b) => b.minimumQuantity - a.minimumQuantity);
    const matchedTier = sortedTiers.find(t => quantity >= t.minimumQuantity);

    let unitPrice = basePriceCents;
    if (matchedTier) {
      if (matchedTier.fixedUnitPriceCents !== undefined) {
        unitPrice = matchedTier.fixedUnitPriceCents;
      } else {
        unitPrice = Math.round((basePriceCents * (100 - matchedTier.discountPercentage)) / 100);
      }
    }

    const subtotalCents = unitPrice * quantity;
    const undiscountedSubtotal = basePriceCents * quantity;
    const totalSavingsCents = Math.max(0, undiscountedSubtotal - subtotalCents);

    return {
      unitPriceCents: unitPrice,
      subtotalCents,
      totalSavingsCents,
      appliedTier: matchedTier
    };
  }
}
