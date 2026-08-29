export interface InventoryStockEntity {
  id: string;
  sku: string;
  warehouseId: string;
  onHandQuantity: number;
  reservedQuantity: number;
  allocatedQuantity: number;
  safetyStockThreshold: number;
  reorderQuantity: number;
  binLocation?: string;
  version: number; // Optimistic locking
  updatedAt: Date;
}

export interface InventoryReservationEntity {
  id: string;
  reservationCode: string;
  orderId: string;
  sku: string;
  warehouseId: string;
  quantity: number;
  isCommitted: boolean;
  isReleased: boolean;
  expiresAt: Date;
  createdAt: Date;
  updatedAt: Date;
}

export interface WarehouseEntity {
  id: string;
  code: string;
  name: string;
  addressId: string;
  isActive: boolean;
  capacityScore: number;
  createdAt: Date;
  updatedAt: Date;
}
