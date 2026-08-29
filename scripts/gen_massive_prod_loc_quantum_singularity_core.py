import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_quantum_singularity_core():
    print("Generating comprehensive Quantum Singularity Core Modules...")

    # 1. Payment Level 3 Line Item Discount Distributor
    write_file("services/payment-service/src/domain/line-item-discount-distributor.ts", """import { Level3LineItemData } from './level3-card-data-builder.js';

export class LineItemDiscountDistributor {
  public static distributeDiscount(items: Level3LineItemData[], totalDiscountCents: number): Level3LineItemData[] {
    const totalGross = items.reduce((acc, it) => acc + it.totalAmountCents, 0);
    if (totalGross === 0 || totalDiscountCents <= 0) return items;

    let remainingDiscount = totalDiscountCents;
    return items.map((it, idx) => {
      if (idx === items.length - 1) {
        return {
          ...it,
          discountAmountCents: remainingDiscount
        };
      }

      const propDiscount = Math.round((it.totalAmountCents / totalGross) * totalDiscountCents);
      const allocated = Math.min(propDiscount, remainingDiscount);
      remainingDiscount -= allocated;

      return {
        ...it,
        discountAmountCents: allocated
      };
    });
  }
}
""")

    # 2. Inventory Automated Replenishment Multi-Echelon Buffer Synchronizer
    write_file("services/inventory-service/src/domain/multi-echelon-synchronizer.ts", """export interface FacilityInventoryNode {
  facilityId: string;
  facilityType: 'CENTRAL_HUB' | 'REGIONAL_DC' | 'LOCAL_SPOKE';
  sku: string;
  onHandQuantity: number;
  safetyStockTarget: number;
  replenishmentLeadTimeDays: number;
}

export class MultiEchelonSynchronizer {
  public static calculateTransfers(
    centralHub: FacilityInventoryNode,
    regionalDcs: FacilityInventoryNode[]
  ): { targetFacilityId: string; transferQuantity: number }[] {
    const transfers: { targetFacilityId: string; transferQuantity: number }[] = [];
    let hubAvailable = Math.max(0, centralHub.onHandQuantity - centralHub.safetyStockTarget);

    for (const dc of regionalDcs) {
      if (hubAvailable <= 0) break;

      const deficit = Math.max(0, dc.safetyStockTarget - dc.onHandQuantity);
      if (deficit > 0) {
        const qtyToTransfer = Math.min(deficit, hubAvailable);
        transfers.push({
          targetFacilityId: dc.facilityId,
          transferQuantity: qtyToTransfer
        });
        hubAvailable -= qtyToTransfer;
      }
    }

    return transfers;
  }
}
""")

    print("Quantum singularity core modules generated.")

if __name__ == "__main__":
    generate_quantum_singularity_core()
