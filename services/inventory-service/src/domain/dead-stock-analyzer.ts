import { InventoryStockEntity } from '@novacommerce/core-types';

export interface DeadStockAssessment {
  sku: string;
  warehouseId: string;
  onHandQuantity: number;
  daysSinceLastSold: number;
  isDeadStock: boolean;
  recommendedAction: 'HOLD' | 'PROMOTIONAL_DISCOUNT' | 'BUNDLE_CLEARANCE' | 'LIQUIDATE_VENDOR';
  discountSuggestedPercentage: number;
}

export class DeadStockAnalyzer {
  public static evaluateStockVelocity(
    stock: InventoryStockEntity,
    daysSinceLastSold: number,
    deadStockThresholdDays: number = 90
  ): DeadStockAssessment {
    const isDead = daysSinceLastSold >= deadStockThresholdDays && stock.onHandQuantity > 0;

    let action: DeadStockAssessment['recommendedAction'] = 'HOLD';
    let discountPct = 0;

    if (daysSinceLastSold >= 180) {
      action = 'LIQUIDATE_VENDOR';
      discountPct = 60;
    } else if (daysSinceLastSold >= 120) {
      action = 'BUNDLE_CLEARANCE';
      discountPct = 40;
    } else if (daysSinceLastSold >= 90) {
      action = 'PROMOTIONAL_DISCOUNT';
      discountPct = 20;
    }

    return {
      sku: stock.sku,
      warehouseId: stock.warehouseId,
      onHandQuantity: stock.onHandQuantity,
      daysSinceLastSold,
      isDeadStock: isDead,
      recommendedAction: action,
      discountSuggestedPercentage: discountPct
    };
  }
}
