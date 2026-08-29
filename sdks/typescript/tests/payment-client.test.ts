import { PaymentApiClient } from '../src/api/PaymentApiClient.js';

describe('TypeScript SDK: PaymentApiClient Suite', () => {
  let client: PaymentApiClient;

  beforeEach(() => {
    client = new PaymentApiClient('http://localhost:8000', () => 'jwt-token');
  });

  it('should define payment authorization methods', () => {
    expect(client.authorizePayment).toBeDefined();
  });
});
