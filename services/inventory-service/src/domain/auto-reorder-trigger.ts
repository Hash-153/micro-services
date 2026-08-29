import { InventoryStockEntity } from '@novacommerce/core-types';

export interface AutoReorderDecision {
  sku: string;
  warehouseId: string;
  shouldTriggerReorder: boolean;
  orderQuantity: number;
  reason: string;
}

export class AutoReorderTrigger {
  public static evaluateStock(stock: InventoryStockEntity): AutoReorderDecision {
    const effectiveStock = stock.onHandQuantity - stock.reservedQuantity;
    const isBelowSafety = effectiveStock <= stock.safetyStockThreshold;

    if (isBelowSafety) {
      return {
        sku: stock.sku,
        warehouseId: stock.warehouseId,
        shouldTriggerReorder: true,
        orderQuantity: stock.reorderQuantity,
        reason: `Available stock (${effectiveStock}) breached safety stock threshold (${stock.safetyStockThreshold}).`
      };
    }

    return {
      sku: stock.sku,
      warehouseId: stock.warehouseId,
      shouldTriggerReorder: false,
      orderQuantity: 0,
      reason: 'Stock levels within normal operating buffer.'
    };
  }
}
