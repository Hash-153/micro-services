export interface InboundReceivingItem {
  poNumber: string;
  sku: string;
  quantityReceived: number;
}

export interface BackorderedOrderItem {
  orderId: string;
  sku: string;
  quantityNeeded: number;
  priorityScore: number;
}

export interface CrossDockAllocation {
  sku: string;
  poNumber: string;
  orderId: string;
  quantityAllocated: number;
  isDirectCrossDock: boolean;
}

export class CrossDockingPlanner {
  public static planCrossDocking(
    inboundItems: InboundReceivingItem[],
    backorders: BackorderedOrderItem[]
  ): { allocations: CrossDockAllocation[]; remainingInbound: InboundReceivingItem[] } {
    const allocations: CrossDockAllocation[] = [];
    const remainingInbound: InboundReceivingItem[] = JSON.parse(JSON.stringify(inboundItems));

    // Sort backorders by priority score descending
    const sortedBackorders = [...backorders].sort((a, b) => b.priorityScore - a.priorityScore);

    for (const bo of sortedBackorders) {
      let needed = bo.quantityNeeded;

      for (const inbound of remainingInbound) {
        if (inbound.sku === bo.sku && inbound.quantityReceived > 0) {
          const allocate = Math.min(needed, inbound.quantityReceived);
          allocations.push({
            sku: bo.sku,
            poNumber: inbound.poNumber,
            orderId: bo.orderId,
            quantityAllocated: allocate,
            isDirectCrossDock: true
          });

          inbound.quantityReceived -= allocate;
          needed -= allocate;
          if (needed <= 0) break;
        }
      }
    }

    return {
      allocations,
      remainingInbound: remainingInbound.filter(i => i.quantityReceived > 0)
    };
  }
}
