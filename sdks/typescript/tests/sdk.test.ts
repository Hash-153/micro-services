import { NovaCommerceClient } from '../src/index.js';

describe('NovaCommerce TypeScript SDK', () => {
  it('should instantiate SDK with configuration', () => {
    const client = new NovaCommerceClient({ baseUrl: 'http://localhost:8000' });
    expect(client).toBeDefined();
    expect(client.auth).toBeDefined();
    expect(client.catalog).toBeDefined();
    expect(client.orders).toBeDefined();
  });
});
