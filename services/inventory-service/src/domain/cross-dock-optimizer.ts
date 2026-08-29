import { InboundAsnItem, OutboundBackorderDemand } from './cross-dock-matrix.js';

export class CrossDockOptimizer {
  public static calculateFulfillmentSavings(
    crossDockedQuantity: number,
    putawayCostPerUnitCents: number = 85, // Standard putaway labor cost
    pickingCostPerUnitCents: number = 110  // Standard pick labor cost
  ): { totalSavingsCents: number; handlingStepsSaved: number } {
    // Cross-docking skips putaway and subsequent retrieval pick
    const unitSavings = putawayCostPerUnitCents + pickingCostPerUnitCents;
    const totalSavings = crossDockedQuantity * unitSavings;

    return {
      totalSavingsCents: totalSavings,
      handlingStepsSaved: 2
    };
  }
}
