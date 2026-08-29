import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v7():
    print("Generating comprehensive Production V7 Modules...")

    # 1. Order Service EDI 850 Export Engine
    write_file("services/order-service/src/domain/edi-850-generator.ts", """import { OrderEntity } from '@novacommerce/core-types';

export class Edi850Generator {
  public static generateEdi850(order: OrderEntity, senderId: string = 'NOVACOMMERCE', receiverId: string = 'SUPPLIER_EDI'): string {
    const dateStr = new Date(order.createdAt).toISOString().slice(2, 10).replace(/-/g, '');
    const timeStr = new Date(order.createdAt).toTimeString().slice(0, 5).replace(/:/g, '');

    const segments: string[] = [
      `ISA*00*          *00*          *ZZ*${senderId.padEnd(15, ' ')}*ZZ*${receiverId.padEnd(15, ' ')}*${dateStr}*${timeStr}*U*00401*000000001*0*P*>~`,
      `GS*PO*${senderId}*${receiverId}*${dateStr}*${timeStr}*1*X*004010~`,
      `ST*850*0001~`,
      `BEG*00*SA*${order.orderNumber}**${dateStr}~`,
      `REF*IA*${order.userId}~`,
      `DTM*002*${dateStr}~`,
      `N1*ST*${order.shippingAddress.recipientName}*92*${order.shippingAddress.id || 'LOC1'}~`,
      `N3*${order.shippingAddress.streetLine1}~`,
      `N4*${order.shippingAddress.city}*${order.shippingAddress.stateOrProvince}*${order.shippingAddress.postalCode}*${order.shippingAddress.countryCode}~`
    ];

    let lineIndex = 1;
    for (const item of order.items) {
      segments.push(`PO1*${lineIndex}*${item.quantity}*EA*${(item.unitPrice.amount / 100).toFixed(2)}*PE*VP*${item.sku}~`);
      segments.push(`PID*F****${item.productName}~`);
      lineIndex++;
    }

    const totalQty = order.items.reduce((acc, it) => acc + it.quantity, 0);
    segments.push(`CTT*${order.items.length}*${totalQty}~`);
    segments.push(`SE*${segments.length - 2}*0001~`);
    segments.push(`GE*1*1~`);
    segments.push(`IEA*1*000000001~`);

    return segments.join('\\n');
  }
}
""")

    # 2. Inventory Service Cross-Docking Planner
    write_file("services/inventory-service/src/domain/cross-docking-planner.ts", """export interface InboundReceivingItem {
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
""")

    print("Production V7 modules generated.")

if __name__ == "__main__":
    generate_prod_v7()
