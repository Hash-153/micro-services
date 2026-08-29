export interface FacilitySafetyScore {
  warehouseId: string;
  skusBelowSafetyStock: number;
  totalSkusManaged: number;
  healthPercentage: number;
}

export class TargetNetworkScorecard {
  public static computeScore(warehouseId: string, skusBelowSafetyStock: number, totalSkusManaged: number): FacilitySafetyScore {
    const health = totalSkusManaged > 0
      ? ((totalSkusManaged - skusBelowSafetyStock) / totalSkusManaged) * 100
      : 100;

    return {
      warehouseId,
      skusBelowSafetyStock,
      totalSkusManaged,
      healthPercentage: Math.round(health * 10) / 10
    };
  }
}
