import { InventoryStockEntity } from '@novacommerce/core-types';

export interface CycleCountRecord {
  countId: string;
  warehouseId: string;
  sku: string;
  systemOnHandQuantity: number;
  physicalCountQuantity: number;
  discrepancyQuantity: number;
  discrepancyPercentage: number;
  unitCostCents: number;
  totalShrinkageCostCents: number;
  status: 'PENDING_APPROVAL' | 'APPROVED' | 'RECOUNT_REQUESTED';
  countedAt: Date;
}

export class CycleCountManager {
  public static processCount(
    stock: InventoryStockEntity,
    physicalCount: number,
    unitCostCents: number = 1500
  ): CycleCountRecord {
    const discrepancy = physicalCount - stock.onHandQuantity;
    const discrepancyPercent = stock.onHandQuantity > 0 ? (discrepancy / stock.onHandQuantity) * 100 : 0;
    const shrinkageCost = Math.abs(discrepancy) * unitCostCents;

    const needsRecount = Math.abs(discrepancyPercent) > 5.0 || shrinkageCost > 100000; // >5% or >$1000 discrepancy

    return {
      countId: `cnt_${Date.now().toString(36)}`,
      warehouseId: stock.warehouseId,
      sku: stock.sku,
      systemOnHandQuantity: stock.onHandQuantity,
      physicalCountQuantity: physicalCount,
      discrepancyQuantity: discrepancy,
      discrepancyPercentage: Math.round(discrepancyPercent * 100) / 100,
      unitCostCents,
      totalShrinkageCostCents: shrinkageCost,
      status: needsRecount ? 'RECOUNT_REQUESTED' : 'PENDING_APPROVAL',
      countedAt: new Date()
    };
  }
}
