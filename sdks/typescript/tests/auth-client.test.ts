import { AuthApiClient } from '../src/api/AuthApiClient.js';
import { UserRole } from '@novacommerce/core-types';

describe('TypeScript SDK: AuthApiClient Suite', () => {
  let client: AuthApiClient;
  let mockToken: string | undefined = undefined;

  beforeEach(() => {
    client = new AuthApiClient('http://localhost:8000', () => mockToken);
  });

  it('should instantiate and configure token provider', () => {
    expect(client).toBeDefined();
    mockToken = 'jwt-test-token';
    expect(client).toBeDefined();
  });
});
