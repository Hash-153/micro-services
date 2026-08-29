import { ShipmentEntity, ApiResponse } from '@novacommerce/core-types';

export class FulfillmentApiClient {
  private readonly baseUrl: string;
  private tokenProvider: () => string | undefined;

  constructor(baseUrl: string, tokenProvider: () => string | undefined) {
    this.baseUrl = baseUrl;
    this.tokenProvider = tokenProvider;
  }

  public async createShipment(orderId: string, destinationAddress: any, carrier: string = 'FEDEX'): Promise<ShipmentEntity> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/fulfillment/shipments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ orderId, destinationAddress, carrier })
    });
    if (!res.ok) throw new Error(`Create shipment failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<ShipmentEntity>;
    return json.data;
  }
}
