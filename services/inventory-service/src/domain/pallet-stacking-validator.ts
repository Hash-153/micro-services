export interface PalletTierConfig {
  maxTiers: number;
  maxTotalHeightMm: number;
  maxTotalWeightGrams: number;
  palletTareWeightGrams: number;
}

export class PalletStackingValidator {
  private static readonly STANDARD_PALLET: PalletTierConfig = {
    maxTiers: 6,
    maxTotalHeightMm: 1800, // 1.8m standard rack height
    maxTotalWeightGrams: 1000000, // 1,000 kg / 1 metric ton
    palletTareWeightGrams: 25000 // 25kg wooden GMA pallet
  };

  public static validatePallet(
    boxHeightMm: number,
    boxWeightGrams: number,
    boxesPerTier: number,
    tierCount: number
  ): { isSafe: boolean; totalHeightMm: number; totalGrossWeightGrams: number; violationReason?: string } {
    const totalHeight = boxHeightMm * tierCount + 150; // +150mm pallet base
    const totalGrossWeight = boxWeightGrams * boxesPerTier * tierCount + this.STANDARD_PALLET.palletTareWeightGrams;

    if (tierCount > this.STANDARD_PALLET.maxTiers) {
      return {
        isSafe: false,
        totalHeightMm: totalHeight,
        totalGrossWeightGrams: totalGrossWeight,
        violationReason: `Tier count (${tierCount}) exceeds max safe limit (${this.STANDARD_PALLET.maxTiers})`
      };
    }

    if (totalHeight > this.STANDARD_PALLET.maxTotalHeightMm) {
      return {
        isSafe: false,
        totalHeightMm: totalHeight,
        totalGrossWeightGrams: totalGrossWeight,
        violationReason: `Total pallet height (${totalHeight}mm) exceeds max rack clearance (${this.STANDARD_PALLET.maxTotalHeightMm}mm)`
      };
    }

    if (totalGrossWeight > this.STANDARD_PALLET.maxTotalWeightGrams) {
      return {
        isSafe: false,
        totalHeightMm: totalHeight,
        totalGrossWeightGrams: totalGrossWeight,
        violationReason: `Total pallet gross weight (${(totalGrossWeight / 1000).toFixed(1)}kg) exceeds rating (${(this.STANDARD_PALLET.maxTotalWeightGrams / 1000).toFixed(1)}kg)`
      };
    }

    return {
      isSafe: true,
      totalHeightMm: totalHeight,
      totalGrossWeightGrams: totalGrossWeight
    };
  }
}
