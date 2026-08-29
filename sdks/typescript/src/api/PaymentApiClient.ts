import { PaymentTransactionEntity, Currency, ApiResponse } from '@novacommerce/core-types';

export class PaymentApiClient {
  private readonly baseUrl: string;
  private tokenProvider: () => string | undefined;

  constructor(baseUrl: string, tokenProvider: () => string | undefined) {
    this.baseUrl = baseUrl;
    this.tokenProvider = tokenProvider;
  }

  public async authorizePayment(orderId: string, amountCents: number, currency: Currency = Currency.USD): Promise<PaymentTransactionEntity> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/payments/authorize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ orderId, amountCents, currency })
    });
    if (!res.ok) throw new Error(`Payment authorization failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<PaymentTransactionEntity>;
    return json.data;
  }
}
