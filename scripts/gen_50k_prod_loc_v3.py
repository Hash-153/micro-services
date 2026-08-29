import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v3():
    print("Generating comprehensive Production V3 Modules...")

    # 1. Payment Settlement Reconciler & Batch Payout Engine
    write_file("services/payment-service/src/domain/batch-payout-engine.ts", """import { Money, Currency } from '@novacommerce/core-types';

export interface MerchantPayoutBatchItem {
  merchantId: string;
  merchantName: string;
  bankRoutingNumber: string;
  bankAccountNumber: string;
  netPayoutAmountCents: number;
  currency: Currency;
}

export interface NachaAchBatchFile {
  batchId: string;
  totalDebitCents: number;
  totalCreditCents: number;
  entryCount: number;
  achFileContent: string;
  createdAt: Date;
}

export class BatchPayoutEngine {
  public static generateAchFile(items: MerchantPayoutBatchItem[], companyName: string = 'NOVACOMMERCE INC'): NachaAchBatchFile {
    const batchId = `ach_${Date.now().toString(36).toUpperCase()}`;
    const totalCredit = items.reduce((acc, it) => acc + it.netPayoutAmountCents, 0);

    const fileHeader = `101 121000358 199999999 ${new Date().toISOString().slice(2, 10).replace(/-/g, '')} 0945 A 094 101 ${companyName.padEnd(23, ' ')}`;
    const batchHeader = `5200 ${companyName.padEnd(16, ' ')}                    121000358 PPD PAYOUTS   ${new Date().toISOString().slice(2, 10).replace(/-/g, '')} 1 12100035 0000001`;

    const detailLines = items.map((it, idx) => {
      const paddedRouting = it.bankRoutingNumber.slice(0, 8);
      const checkDigit = it.bankRoutingNumber.slice(8, 9) || '0';
      const paddedAccount = it.bankAccountNumber.padEnd(17, ' ');
      const paddedAmount = it.netPayoutAmountCents.toString().padStart(10, '0');
      const paddedId = it.merchantId.slice(0, 15).padEnd(15, ' ');
      const paddedName = it.merchantName.slice(0, 22).padEnd(22, ' ');

      return `622 ${paddedRouting}${checkDigit} ${paddedAccount} ${paddedAmount} ${paddedId} ${paddedName} 00 12100035${(idx + 1).toString().padStart(7, '0')}`;
    });

    const batchControl = `8200 ${items.length.toString().padStart(6, '0')} 0000000000 0000000000 ${totalCredit.toString().padStart(12, '0')} 199999999           12100035 0000001`;
    const fileControl = `9000001 000001 ${(items.length + 4).toString().padStart(6, '0')} 0000000000 0000000000 ${totalCredit.toString().padStart(12, '0')}                        `;

    const fullAch = [fileHeader, batchHeader, ...detailLines, batchControl, fileControl].join('\\n');

    return {
      batchId,
      totalDebitCents: 0,
      totalCreditCents: totalCredit,
      entryCount: items.length,
      achFileContent: fullAch,
      createdAt: new Date()
    };
  }
}
""")

    # 2. Fulfillment Split Order Dispatch Planner
    write_file("services/fulfillment-service/src/domain/split-order-planner.ts", """import { OrderEntity, OrderItemEntity } from '@novacommerce/core-types';

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
""")

    print("Production V3 modules generated.")

if __name__ == "__main__":
    generate_prod_v3()
