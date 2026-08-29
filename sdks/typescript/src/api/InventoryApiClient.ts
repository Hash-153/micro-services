import { InventoryStockEntity, InventoryReservationEntity, ApiResponse } from '@novacommerce/core-types';

export class InventoryApiClient {
  private readonly baseUrl: string;
  private tokenProvider: () => string | undefined;

  constructor(baseUrl: string, tokenProvider: () => string | undefined) {
    this.baseUrl = baseUrl;
    this.tokenProvider = tokenProvider;
  }

  public async setStock(sku: string, warehouseId: string, quantity: number): Promise<InventoryStockEntity> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/inventory/stock`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ sku, warehouseId, quantity })
    });
    if (!res.ok) throw new Error(`Set stock failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<InventoryStockEntity>;
    return json.data;
  }

  public async reserveStock(orderId: string, sku: string, quantity: number): Promise<InventoryReservationEntity> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/inventory/reserve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ orderId, sku, quantity })
    });
    if (!res.ok) throw new Error(`Reserve stock failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<InventoryReservationEntity>;
    return json.data;
  }
}
