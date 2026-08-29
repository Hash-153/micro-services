export interface StockDemandParameters {
  sku: string;
  dailyDemandMean: number;
  dailyDemandVariance: number;
  leadTimeDaysMean: number;
  leadTimeDaysVariance: number;
  targetServiceLevelPercent: number; // e.g. 95 or 99
}

export class SafetyStockMatrixCalculator {
  private static readonly Z_SCORE_TABLE: Record<number, number> = {
    90: 1.282,
    95: 1.645,
    98: 2.054,
    99: 2.326,
    99.9: 3.090
  };

  public static calculateComprehensiveSafetyStock(params: StockDemandParameters): {
    safetyStockUnits: number;
    reorderPointUnits: number;
    serviceLevelZScore: number;
    combinedStandardDeviation: number;
  } {
    const zScore = this.Z_SCORE_TABLE[params.targetServiceLevelPercent] || 1.645;

    // Combined variance formula: Var(Demand during Lead Time) = L * Var(D) + D^2 * Var(L)
    const demandVariance = params.dailyDemandVariance;
    const leadTimeVariance = params.leadTimeDaysVariance;
    const meanDemand = params.dailyDemandMean;
    const meanLeadTime = params.leadTimeDaysMean;

    const totalVariance = meanLeadTime * demandVariance + Math.pow(meanDemand, 2) * leadTimeVariance;
    const combinedStdDev = Math.sqrt(Math.max(0, totalVariance));

    const safetyStockUnits = Math.ceil(zScore * combinedStdDev);
    const reorderPointUnits = Math.ceil(meanDemand * meanLeadTime + safetyStockUnits);

    return {
      safetyStockUnits,
      reorderPointUnits,
      serviceLevelZScore: zScore,
      combinedStandardDeviation: Math.round(combinedStdDev * 100) / 100
    };
  }
}
