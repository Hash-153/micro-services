import { SkuDemandDistribution, SafetyStockBufferCalculator } from './safety-stock-buffer-calculator.js';

export class SafetyStockReviewer {
  public static auditStockLevel(
    currentOnHand: number,
    currentSafetyStock: number,
    demandDist: SkuDemandDistribution
  ): { needsAdjustment: boolean; recommendedSafetyStock: number; differenceUnits: number; reason: string } {
    const calc = SafetyStockBufferCalculator.calculateBuffer(demandDist);
    const recommended = calc.safetyStockUnits;
    const diff = recommended - currentSafetyStock;

    if (Math.abs(diff) >= 5) {
      return {
        needsAdjustment: true,
        recommendedSafetyStock: recommended,
        differenceUnits: diff,
        reason: diff > 0
          ? `Demand volatility or lead time variance increased; increase safety stock by +${diff} units.`
          : `Demand stabilized; release ${Math.abs(diff)} units from safety reserve to reduce holding costs.`
      };
    }

    return {
      needsAdjustment: false,
      recommendedSafetyStock: currentSafetyStock,
      differenceUnits: 0,
      reason: 'Current safety stock matches statistical demand distribution within tolerance.'
    };
  }
}
