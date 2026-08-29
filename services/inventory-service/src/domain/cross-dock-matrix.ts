export interface InboundAsnItem {
  sku: string;
  quantity: number;
  asnNumber: string;
}

export interface OutboundBackorderDemand {
  sku: string;
  orderId: string;
  backorderQuantity: number;
  priorityScore: number;
}

export class CrossDockDecisionMatrix {
  public static planCrossDocking(
    inbound: InboundAsnItem[],
    backorders: OutboundBackorderDemand[]
  ): { sku: string; orderId: string; quantityToCrossDock: number }[] {
    const crossDocks: { sku: string; orderId: string; quantityToCrossDock: number }[] = [];

    for (const inItem of inbound) {
      let remainingInbound = inItem.quantity;
      const matchingBackorders = backorders
        .filter(b => b.sku === inItem.sku)
        .sort((a, b) => b.priorityScore - a.priorityScore);

      for (const bo of matchingBackorders) {
        if (remainingInbound <= 0) break;

        const dockQty = Math.min(remainingInbound, bo.backorderQuantity);
        crossDocks.push({
          sku: inItem.sku,
          orderId: bo.orderId,
          quantityToCrossDock: dockQty
        });

        remainingInbound -= dockQty;
        bo.backorderQuantity -= dockQty;
      }
    }

    return crossDocks;
  }
}
