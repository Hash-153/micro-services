import { OrderEntity, CreateOrderDTO, ApiResponse } from '@novacommerce/core-types';

export class OrderApiClient {
  private readonly baseUrl: string;
  private tokenProvider: () => string | undefined;

  constructor(baseUrl: string, tokenProvider: () => string | undefined) {
    this.baseUrl = baseUrl;
    this.tokenProvider = tokenProvider;
  }

  public async createOrder(dto: CreateOrderDTO): Promise<OrderEntity> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/orders`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(dto)
    });
    if (!res.ok) throw new Error(`Create order failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<OrderEntity>;
    return json.data;
  }

  public async getOrderById(id: string): Promise<OrderEntity> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/orders/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!res.ok) throw new Error(`Get order failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<OrderEntity>;
    return json.data;
  }
}
