export interface AgingStockRecord {
  sku: string;
  onHandUnits: number;
  daysWithoutSale: number;
  unitCostCents: number;
  holdingCostPerUnitPerMonthCents: number;
}

export class LiquidationRecommender {
  public static evaluateLiquidation(record: AgingStockRecord): { shouldLiquidate: boolean; recommendedDiscountPercent: number; estimatedHoldingLossCents: number } {
    const monthsStagnant = record.daysWithoutSale / 30;
    const totalHoldingCost = record.onHandUnits * record.holdingCostPerUnitPerMonthCents * monthsStagnant;

    if (record.daysWithoutSale > 180) {
      return {
        shouldLiquidate: true,
        recommendedDiscountPercent: 50,
        estimatedHoldingLossCents: Math.round(totalHoldingCost)
      };
    }

    if (record.daysWithoutSale > 90) {
      return {
        shouldLiquidate: true,
        recommendedDiscountPercent: 25,
        estimatedHoldingLossCents: Math.round(totalHoldingCost)
      };
    }

    return {
      shouldLiquidate: false,
      recommendedDiscountPercent: 0,
      estimatedHoldingLossCents: Math.round(totalHoldingCost)
    };
  }
}
