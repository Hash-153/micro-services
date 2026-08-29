import { OrderApiClient } from '../src/api/OrderApiClient.js';

describe('TypeScript SDK: OrderApiClient Suite', () => {
  let client: OrderApiClient;

  beforeEach(() => {
    client = new OrderApiClient('http://localhost:8000', () => 'jwt-token');
  });

  it('should define order lifecycle methods', () => {
    expect(client.createOrder).toBeDefined();
    expect(client.getOrderById).toBeDefined();
  });
});
