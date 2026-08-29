export interface WarehouseStorageLocation {
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
