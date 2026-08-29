import { OrderEntity, OrderItemEntity } from '@novacommerce/core-types';

export interface SkuWarehouseAvailability {
  sku: string;
  warehouseId: string;
  availableQuantity: number;
}

export interface SplitShipmentPlan {
  orderId: string;
  shipments: {
    warehouseId: string;
    items: { sku: string; quantity: number }[];
  }[];
  isSplitOrder: boolean;
}

export class SplitOrderPlanner {
  public static planSplitFulfillment(
    order: OrderEntity,
    availabilities: SkuWarehouseAvailability[]
  ): SplitShipmentPlan {
    const warehouseAssignments: Map<string, { sku: string; quantity: number }[]> = new Map();

    for (const item of order.items) {
      let needed = item.quantity;
      const skuStock = availabilities
        .filter(a => a.sku === item.sku && a.availableQuantity > 0)
        .sort((a, b) => b.availableQuantity - a.availableQuantity);

      for (const stock of skuStock) {
        if (needed <= 0) break;
        const take = Math.min(needed, stock.availableQuantity);
        if (!warehouseAssignments.has(stock.warehouseId)) {
          warehouseAssignments.set(stock.warehouseId, []);
        }
        warehouseAssignments.get(stock.warehouseId)!.push({ sku: item.sku, quantity: take });
        needed -= take;
        stock.availableQuantity -= take;
      }

      if (needed > 0) {
        throw new Error(`Insufficient aggregate stock across all fulfillment centers for SKU ${item.sku} (needed: ${needed})`);
      }
    }

    const shipments = Array.from(warehouseAssignments.entries()).map(([warehouseId, items]) => ({
      warehouseId,
      items
    }));

    return {
      orderId: order.id,
      shipments,
      isSplitOrder: shipments.length > 1
    };
  }
}
