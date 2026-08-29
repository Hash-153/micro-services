export interface InventoryDemandForecast {
  sku: string;
  averageDailySales: number;
  leadTimeDays: number;
  supplierReliabilityPercent: number; // 0 to 100
  serviceLevelZScore: number; // e.g. 1.65 for 95%, 2.33 for 99%
  demandStandardDeviation: number;
}

export interface ReorderRecommendation {
  sku: string;
  safetyStockUnits: number;
  reorderPointUnits: number;
  economicOrderQuantity: number;
  suggestedAction: 'ORDER_NOW' | 'STOCK_HEALTHY' | 'SURPLUS';
}

export class ReorderCalculator {
  // Uses Wilson EOQ (Economic Order Quantity) & probabilistic Safety Stock formulas
  public static calculateReorderParameters(
    forecast: InventoryDemandForecast,
    currentOnHand: number,
    currentReserved: number,
    annualCarryingCostPerUnit: number = 5.0,
    fixedOrderPlacementCost: number = 50.0
  ): ReorderRecommendation {
    // Safety Stock = Z * stdDev * sqrt(LeadTime)
    const safetyStock = Math.ceil(
      forecast.serviceLevelZScore * forecast.demandStandardDeviation * Math.sqrt(forecast.leadTimeDays)
    );

    // Reorder Point = (Daily Demand * Lead Time) + Safety Stock
    const leadTimeDemand = forecast.averageDailySales * forecast.leadTimeDays;
    const reorderPoint = Math.ceil(leadTimeDemand + safetyStock);

    // Economic Order Quantity (EOQ) = sqrt((2 * Annual Demand * Order Cost) / Carrying Cost)
    const annualDemand = forecast.averageDailySales * 365;
    const eoq = Math.ceil(
      Math.sqrt((2 * annualDemand * fixedOrderPlacementCost) / annualCarryingCostPerUnit)
    );

    const availableStock = currentOnHand - currentReserved;
    let suggestedAction: 'ORDER_NOW' | 'STOCK_HEALTHY' | 'SURPLUS' = 'STOCK_HEALTHY';

    if (availableStock <= reorderPoint) {
      suggestedAction = 'ORDER_NOW';
    } else if (availableStock > reorderPoint * 3) {
      suggestedAction = 'SURPLUS';
    }

    return {
      sku: forecast.sku,
      safetyStockUnits: safetyStock,
      reorderPointUnits: reorderPoint,
      economicOrderQuantity: eoq,
      suggestedAction
    };
  }
}
