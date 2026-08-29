export interface WarehouseBinLocation {
  binId: string;
  zone: string;
  aisle: number;
  shelf: number;
  position: number;
}

export interface PickItem {
  sku: string;
  quantity: number;
  binLocation: WarehouseBinLocation;
}

export class AisleGraphOptimizer {
  public static calculateOptimalPickPath(items: PickItem[]): PickItem[] {
    // Sorts by S-shape picking trajectory across warehouse aisles
    return [...items].sort((a, b) => {
      // 1. Zone sorting
      if (a.binLocation.zone !== b.binLocation.zone) {
        return a.binLocation.zone.localeCompare(b.binLocation.zone);
      }

      // 2. Aisle sorting
      if (a.binLocation.aisle !== b.binLocation.aisle) {
        return a.binLocation.aisle - b.binLocation.aisle;
      }

      // 3. S-shape serpentine direction: even aisles go forward, odd aisles go backwards
      const isEvenAisle = a.binLocation.aisle % 2 === 0;
      if (isEvenAisle) {
        if (a.binLocation.shelf !== b.binLocation.shelf) {
          return a.binLocation.shelf - b.binLocation.shelf;
        }
        return a.binLocation.position - b.binLocation.position;
      } else {
        if (a.binLocation.shelf !== b.binLocation.shelf) {
          return b.binLocation.shelf - a.binLocation.shelf;
        }
        return b.binLocation.position - a.binLocation.position;
      }
    });
  }
}
