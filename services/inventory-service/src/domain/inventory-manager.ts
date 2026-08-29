import { InventoryStockEntity, InventoryReservationEntity, WarehouseEntity } from '@novacommerce/core-types';

export interface StockLevel {
  sku: string;
  warehouseId: string;
  onHand: number;
  available: number;
  reserved: number;
  allocated: number;
  incoming: number;
  reorderPoint: number;
  status: 'IN_STOCK' | 'LOW_STOCK' | 'OUT_OF_STOCK' | 'OVERSTOCK';
}

export interface ReservationRequest {
  orderId: string;
  items: { sku: string; quantity: number; warehouseId?: string }[];
  expiresAt?: Date;
}

export interface ReservationResult {
  success: boolean;
  reservationCode?: string;
  errors: { sku: string; reason: string }[];
  reservedItems: { sku: string; quantity: number; warehouseId: string }[];
}

export class InventoryManager {
  private stock: Map<string, InventoryStockEntity> = new Map();
  private reservations: Map<string, InventoryReservationEntity> = new Map();
  private warehouses: Map<string, WarehouseEntity> = new Map();

  constructor() {
    this.initializeWarehouses();
    this.initializeStock();
  }

  private initializeWarehouses(): void {
    const warehouses: WarehouseEntity[] = [
      {
        id: 'wh-001',
        code: 'US-WEST-1',
        name: 'West Coast Distribution Center',
        latitude: 37.7749,
        longitude: -122.4194,
        address: {
          id: 'addr-001',
          recipientName: 'NovaCommerce West',
          streetLine1: '1234 Industrial Blvd',
          city: 'San Francisco',
          stateOrProvince: 'CA',
          postalCode: '94107',
          countryCode: 'US',
          isDefaultShipping: false,
          isDefaultBilling: false,
          createdAt: new Date(),
          updatedAt: new Date()
        },
        isActive: true,
        capacityScore: 95,
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        id: 'wh-002',
        code: 'US-EAST-1',
        name: 'East Coast Distribution Center',
        latitude: 40.7128,
        longitude: -74.0060,
        address: {
          id: 'addr-002',
          recipientName: 'NovaCommerce East',
          streetLine1: '5678 Logistics Way',
          city: 'Newark',
          stateOrProvince: 'NJ',
          postalCode: '07102',
          countryCode: 'US',
          isDefaultShipping: false,
          isDefaultBilling: false,
          createdAt: new Date(),
          updatedAt: new Date()
        },
        isActive: true,
        capacityScore: 88,
        createdAt: new Date(),
        updatedAt: new Date()
      }
    ];

    warehouses.forEach(wh => this.warehouses.set(wh.id, wh));
  }

  private initializeStock(): void {
    const initialStock: InventoryStockEntity[] = [
      {
        id: 'stock-001',
        sku: 'LAPTOP-PRO-001',
        warehouseId: 'wh-001',
        onHandQuantity: 150,
        reservedQuantity: 25,
        allocatedQuantity: 10,
        safetyStockThreshold: 20,
        reorderQuantity: 50,
        binLocation: 'A-12-34',
        version: 1,
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        id: 'stock-002',
        sku: 'LAPTOP-PRO-001',
        warehouseId: 'wh-002',
        onHandQuantity: 200,
        reservedQuantity: 30,
        allocatedQuantity: 15,
        safetyStockThreshold: 25,
        reorderQuantity: 75,
        binLocation: 'B-56-78',
        version: 1,
        createdAt: new Date(),
        updatedAt: new Date()
      }
    ];

    initialStock.forEach(stock => {
      this.stock.set(`${stock.sku}-${stock.warehouseId}`, stock);
    });
  }

  public async getStockLevel(sku: string, warehouseId?: string): Promise<StockLevel[]> {
    const results: StockLevel[] = [];

    if (warehouseId) {
      const key = `${sku}-${warehouseId}`;
      const stock = this.stock.get(key);
      if (stock) {
        results.push(this.calculateStockLevel(stock));
      }
    } else {
      // Get stock across all warehouses
      for (const [key, stock] of this.stock.entries()) {
        if (key.startsWith(sku)) {
          results.push(this.calculateStockLevel(stock));
        }
      }
    }

    return results;
  }

  private calculateStockLevel(stock: InventoryStockEntity): StockLevel {
    const available = stock.onHandQuantity - stock.reservedQuantity - stock.allocatedQuantity;
    const reorderPoint = stock.safetyStockThreshold;
    
    let status: StockLevel['status'] = 'IN_STOCK';
    if (available === 0) {
      status = 'OUT_OF_STOCK';
    } else if (available < reorderPoint) {
      status = 'LOW_STOCK';
    } else if (available > reorderPoint * 3) {
      status = 'OVERSTOCK';
    }

    return {
      sku: stock.sku,
      warehouseId: stock.warehouseId,
      onHand: stock.onHandQuantity,
      available,
      reserved: stock.reservedQuantity,
      allocated: stock.allocatedQuantity,
      incoming: 0, // Would be calculated from incoming transfers
      reorderPoint,
      status
    };
  }

  public async reserveInventory(request: ReservationRequest): Promise<ReservationResult> {
    const reservationCode = `RES-${Date.now()}-${Math.random().toString(36).substr(2, 9).toUpperCase()}`;
    const errors: { sku: string; reason: string }[] = [];
    const reservedItems: { sku: string; quantity: number; warehouseId: string }[] = [];

    for (const item of request.items) {
      const warehouseId = item.warehouseId || this.findBestWarehouse(item.sku, item.quantity);
      const key = `${item.sku}-${warehouseId}`;
      const stock = this.stock.get(key);

      if (!stock) {
        errors.push({ sku: item.sku, reason: 'No stock found for SKU' });
        continue;
      }

      const available = stock.onHandQuantity - stock.reservedQuantity - stock.allocatedQuantity;
      if (available < item.quantity) {
        errors.push({ sku: item.sku, reason: `Insufficient stock: ${available} available, ${item.quantity} requested` });
        continue;
      }

      // Create reservation
      const reservation: InventoryReservationEntity = {
        id: `res-${Date.now()}`,
        reservationCode,
        orderId: request.orderId,
        sku: item.sku,
        warehouseId,
        quantity: item.quantity,
        isCommitted: false,
        isReleased: false,
        expiresAt: request.expiresAt || new Date(Date.now() + 24 * 60 * 60 * 1000), // 24 hours default
        createdAt: new Date(),
        updatedAt: new Date()
      };

      this.reservations.set(reservation.id, reservation);

      // Update stock
      stock.reservedQuantity += item.quantity;
      stock.version++;
      this.stock.set(key, stock);

      reservedItems.push({
        sku: item.sku,
        quantity: item.quantity,
        warehouseId
      });
    }

    return {
      success: errors.length === 0,
      reservationCode: errors.length === 0 ? reservationCode : undefined,
      errors,
      reservedItems
    };
  }

  private findBestWarehouse(sku: string, quantity: number): string {
    // Simple logic: find warehouse with most available stock
    let bestWarehouse = '';
    let maxAvailable = -1;

    for (const [key, stock] of this.stock.entries()) {
      if (key.startsWith(sku)) {
        const available = stock.onHandQuantity - stock.reservedQuantity - stock.allocatedQuantity;
        if (available >= quantity && available > maxAvailable) {
          maxAvailable = available;
          bestWarehouse = stock.warehouseId;
        }
      }
    }

    return bestWarehouse || this.warehouses.keys().next().value || '';
  }

  public async commitReservation(reservationCode: string): Promise<boolean> {
    for (const reservation of this.reservations.values()) {
      if (reservation.reservationCode === reservationCode && !reservation.isReleased) {
        reservation.isCommitted = true;
        reservation.isReleased = true;

        const key = `${reservation.sku}-${reservation.warehouseId}`;
        const stock = this.stock.get(key);
        if (stock) {
          stock.reservedQuantity -= reservation.quantity;
          stock.allocatedQuantity += reservation.quantity;
          stock.version++;
          this.stock.set(key, stock);
        }

        return true;
      }
    }
    return false;
  }

  public async releaseReservation(reservationCode: string): Promise<boolean> {
    for (const reservation of this.reservations.values()) {
      if (reservation.reservationCode === reservationCode && !reservation.isReleased) {
        reservation.isReleased = true;

        const key = `${reservation.sku}-${reservation.warehouseId}`;
        const stock = this.stock.get(key);
        if (stock) {
          stock.reservedQuantity -= reservation.quantity;
          stock.version++;
          this.stock.set(key, stock);
        }

        return true;
      }
    }
    return false;
  }

  public async adjustStock(sku: string, warehouseId: string, quantity: number, reason: string): Promise<void> {
    const key = `${sku}-${warehouseId}`;
    const stock = this.stock.get(key);

    if (stock) {
      stock.onHandQuantity += quantity;
      stock.version++;
      stock.updatedAt = new Date();
      this.stock.set(key, stock);
    } else {
      // Create new stock record
      const newStock: InventoryStockEntity = {
        id: `stock-${Date.now()}`,
        sku,
        warehouseId,
        onHandQuantity: Math.max(0, quantity),
        reservedQuantity: 0,
        allocatedQuantity: 0,
        safetyStockThreshold: 10,
        reorderQuantity: 25,
        version: 1,
        createdAt: new Date(),
        updatedAt: new Date()
      };
      this.stock.set(key, newStock);
    }
  }
}
