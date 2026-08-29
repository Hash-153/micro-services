export interface SkuDemandDistribution {
  sku: string;
  averageDailySales: number;
  salesStandardDeviation: number;
  leadTimeDays: number;
  leadTimeStandardDeviation: number;
  serviceFactorZ: number; // 1.65 for 95%, 2.33 for 99%
}

export class SafetyStockBufferCalculator {
  public static calculateBuffer(dist: SkuDemandDistribution): { safetyStockUnits: number; bufferExplanation: string } {
    // Formula: SS = Z * sqrt( (LT * sigma_D^2) + (D^2 * sigma_LT^2) )
    const term1 = dist.leadTimeDays * Math.pow(dist.salesStandardDeviation, 2);
    const term2 = Math.pow(dist.averageDailySales, 2) * Math.pow(dist.leadTimeStandardDeviation, 2);
    const combinedStdDev = Math.sqrt(term1 + term2);
    const safetyStock = Math.ceil(dist.serviceFactorZ * combinedStdDev);

    return {
      safetyStockUnits: Math.max(1, safetyStock),
      bufferExplanation: `Safety stock calculated with Z=${dist.serviceFactorZ} over LT=${dist.leadTimeDays}d (+/-${dist.leadTimeStandardDeviation}d)`
    };
  }
}
