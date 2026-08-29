import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_quantum_nebula_modules():
    print("Generating comprehensive Quantum Nebula Modules...")

    # 1. Payment Merchant Settlement Reconciliation Report Generator
    write_file("services/payment-service/src/domain/merchant-reconciliation-report.ts", """import { Money, Currency } from '@novacommerce/core-types';

export interface SettlementBatchItem {
  transactionId: string;
  orderNumber: string;
  grossAmountCents: number;
  interchangeFeeCents: number;
  gatewayFeeCents: number;
  netPayoutCents: number;
  settledDate: string;
}

export class MerchantReconciliationReport {
  public static generateSummary(items: SettlementBatchItem[], currency: Currency = Currency.USD): {
    totalGrossAmountCents: number;
    totalInterchangeCents: number;
    totalGatewayFeeCents: number;
    totalNetPayoutCents: number;
    transactionCount: number;
    effectiveProcessingRatePercent: number;
  } {
    const totalGross = items.reduce((acc, it) => acc + it.grossAmountCents, 0);
    const totalInterchange = items.reduce((acc, it) => acc + it.interchangeFeeCents, 0);
    const totalGatewayFee = items.reduce((acc, it) => acc + it.gatewayFeeCents, 0);
    const totalNetPayout = items.reduce((acc, it) => acc + it.netPayoutCents, 0);
    const totalFees = totalInterchange + totalGatewayFee;

    const rate = totalGross > 0 ? (totalFees / totalGross) * 100 : 0;

    return {
      totalGrossAmountCents: totalGross,
      totalInterchangeCents: totalInterchange,
      totalGatewayFeeCents: totalGatewayFee,
      totalNetPayoutCents: totalNetPayout,
      transactionCount: items.length,
      effectiveProcessingRatePercent: Math.round(rate * 100) / 100
    };
  }
}
""")

    # 2. Inventory Multi-Bin SKU Consolidation Planner
    write_file("services/inventory-service/src/domain/bin-consolidation-planner.ts", """export interface FragmentedBinStock {
  binId: string;
  sku: string;
  quantity: number;
  maxBinCapacity: number;
}

export class BinConsolidationPlanner {
  public static planConsolidation(bins: FragmentedBinStock[]): { sourceBinId: string; targetBinId: string; quantityToMove: number }[] {
    const moves: { sourceBinId: string; targetBinId: string; quantityToMove: number }[] = [];
    const groupedBySku = new Map<string, FragmentedBinStock[]>();

    for (const b of bins) {
      if (!groupedBySku.has(b.sku)) {
        groupedBySku.set(b.sku, []);
      }
      groupedBySku.get(b.sku)!.push({ ...b });
    }

    for (const [sku, skuBins] of groupedBySku.entries()) {
      if (skuBins.length <= 1) continue;

      // Sort bins ascending by current quantity (drain lowest bins first)
      skuBins.sort((a, b) => a.quantity - b.quantity);

      let targetIdx = skuBins.length - 1;
      let sourceIdx = 0;

      while (sourceIdx < targetIdx) {
        const source = skuBins[sourceIdx];
        const target = skuBins[targetIdx];

        const spaceInTarget = target.maxBinCapacity - target.quantity;
        if (spaceInTarget <= 0) {
          targetIdx--;
          continue;
        }

        const moveQty = Math.min(source.quantity, spaceInTarget);
        if (moveQty > 0) {
          moves.push({
            sourceBinId: source.binId,
            targetBinId: target.binId,
            quantityToMove: moveQty
          });
          source.quantity -= moveQty;
          target.quantity += moveQty;
        }

        if (source.quantity === 0) {
          sourceIdx++;
        }
        if (target.quantity >= target.maxBinCapacity) {
          targetIdx--;
        }
      }
    }

    return moves;
  }
}
""")

    print("Quantum nebula modules generated.")

if __name__ == "__main__":
    generate_quantum_nebula_modules()
