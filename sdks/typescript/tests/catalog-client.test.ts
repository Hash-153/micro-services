import { CatalogApiClient } from '../src/api/CatalogApiClient.js';

describe('TypeScript SDK: CatalogApiClient Suite', () => {
  let client: CatalogApiClient;

  beforeEach(() => {
    client = new CatalogApiClient('http://localhost:8000', () => 'jwt-token');
  });

  it('should define catalog query methods', () => {
    expect(client.listProducts).toBeDefined();
    expect(client.getProductById).toBeDefined();
    expect(client.createProduct).toBeDefined();
  });
});
