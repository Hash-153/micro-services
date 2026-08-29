export interface WarehouseStorageAisle {
  aisleNumber: number;
  zoneId: string;
  totalShelves: number;
  binsPerShelf: number;
  shelfWeightCapacityGrams: number;
}

export const WAREHOUSE_AISLE_MAPS: WarehouseStorageAisle[] = [
  { aisleNumber: 1, zoneId: 'ZONE-A-FAST', totalShelves: 5, binsPerShelf: 10, shelfWeightCapacityGrams: 500000 },
  { aisleNumber: 2, zoneId: 'ZONE-A-FAST', totalShelves: 5, binsPerShelf: 10, shelfWeightCapacityGrams: 500000 },
  { aisleNumber: 3, zoneId: 'ZONE-A-FAST', totalShelves: 5, binsPerShelf: 10, shelfWeightCapacityGrams: 500000 },
  { aisleNumber: 4, zoneId: 'ZONE-B-BULK', totalShelves: 4, binsPerShelf: 6, shelfWeightCapacityGrams: 2000000 },
  { aisleNumber: 5, zoneId: 'ZONE-B-BULK', totalShelves: 4, binsPerShelf: 6, shelfWeightCapacityGrams: 2000000 },
  { aisleNumber: 6, zoneId: 'ZONE-B-BULK', totalShelves: 4, binsPerShelf: 6, shelfWeightCapacityGrams: 2000000 },
  { aisleNumber: 7, zoneId: 'ZONE-C-COLD', totalShelves: 4, binsPerShelf: 8, shelfWeightCapacityGrams: 800000 },
  { aisleNumber: 8, zoneId: 'ZONE-C-COLD', totalShelves: 4, binsPerShelf: 8, shelfWeightCapacityGrams: 800000 },
  { aisleNumber: 9, zoneId: 'ZONE-D-HAZMAT', totalShelves: 3, binsPerShelf: 4, shelfWeightCapacityGrams: 1000000 },
  { aisleNumber: 10, zoneId: 'ZONE-D-HAZMAT', totalShelves: 3, binsPerShelf: 4, shelfWeightCapacityGrams: 1000000 }
];

export class WarehouseAisleDirectory {
  public static getAisle(aisleNumber: number): WarehouseStorageAisle | undefined {
    return WAREHOUSE_AISLE_MAPS.find(a => a.aisleNumber === aisleNumber);
  }
}
