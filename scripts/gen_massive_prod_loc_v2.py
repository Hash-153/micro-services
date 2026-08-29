import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v2():
    print("Generating comprehensive Production V2 Modules...")

    # 1. Product Price Tier Volume Discounts Engine
    write_file("services/catalog-service/src/domain/price-tier-engine.ts", """import { Money, Currency } from '@novacommerce/core-types';

export interface VolumePriceTier {
  minimumQuantity: number;
  discountPercentage: number;
  fixedUnitPriceCents?: number;
}

export class PriceTierEngine {
  public static calculateTieredPrice(
    basePriceCents: number,
    quantity: number,
    tiers: VolumePriceTier[]
  ): { unitPriceCents: number; subtotalCents: number; totalSavingsCents: number; appliedTier?: VolumePriceTier } {
    const sortedTiers = [...tiers].sort((a, b) => b.minimumQuantity - a.minimumQuantity);
    const matchedTier = sortedTiers.find(t => quantity >= t.minimumQuantity);

    let unitPrice = basePriceCents;
    if (matchedTier) {
      if (matchedTier.fixedUnitPriceCents !== undefined) {
        unitPrice = matchedTier.fixedUnitPriceCents;
      } else {
        unitPrice = Math.round((basePriceCents * (100 - matchedTier.discountPercentage)) / 100);
      }
    }

    const subtotalCents = unitPrice * quantity;
    const undiscountedSubtotal = basePriceCents * quantity;
    const totalSavingsCents = Math.max(0, undiscountedSubtotal - subtotalCents);

    return {
      unitPriceCents: unitPrice,
      subtotalCents,
      totalSavingsCents,
      appliedTier: matchedTier
    };
  }
}
""")

    # 2. Inventory Bin Placement Algorithm
    write_file("services/inventory-service/src/domain/bin-placement-engine.ts", """export interface WarehouseStorageLocation {
  locationCode: string;
  zone: string;
  volumeCapacityCubicMm: number;
  maxWeightGrams: number;
  currentVolumeUsedCubicMm: number;
  currentWeightGrams: number;
  isHazardousMaterialAllowed: boolean;
  temperatureControlled: boolean;
}

export interface ItemPhysicalSpec {
  sku: string;
  volumeCubicMm: number;
  weightGrams: number;
  isHazardous: boolean;
  requiresRefrigeration: boolean;
}

export class BinPlacementEngine {
  public static findSuitableBins(
    item: ItemPhysicalSpec,
    bins: WarehouseStorageLocation[],
    quantity: number = 1
  ): WarehouseStorageLocation[] {
    const requiredVolume = item.volumeCubicMm * quantity;
    const requiredWeight = item.weightGrams * quantity;

    return bins.filter(bin => {
      if (item.isHazardous && !bin.isHazardousMaterialAllowed) return false;
      if (item.requiresRefrigeration && !bin.temperatureControlled) return false;

      const remainingVolume = bin.volumeCapacityCubicMm - bin.currentVolumeUsedCubicMm;
      const remainingWeight = bin.maxWeightGrams - bin.currentWeightGrams;

      return remainingVolume >= requiredVolume && remainingWeight >= requiredWeight;
    }).sort((a, b) => {
      // Best fit: choose the bin with smallest remaining capacity that fits
      const remainingA = a.volumeCapacityCubicMm - a.currentVolumeUsedCubicMm;
      const remainingB = b.volumeCapacityCubicMm - b.currentVolumeUsedCubicMm;
      return remainingA - remainingB;
    });
  }
}
""")

    print("Production V2 modules generated.")

if __name__ == "__main__":
    generate_prod_v2()
