export interface FacilitySafetyStockTarget {
  warehouseId: string;
  sku: string;
  safetyStockUnits: number;
}

export class TargetMultifacilityAggregator {
  public static aggregateNetworkSafetyStock(targets: FacilitySafetyStockTarget[]): Map<string, number> {
    const skuTotals = new Map<string, number>();

    for (const t of targets) {
      skuTotals.set(t.sku, (skuTotals.get(t.sku) || 0) + t.safetyStockUnits);
    }

    return skuTotals;
  }
}
