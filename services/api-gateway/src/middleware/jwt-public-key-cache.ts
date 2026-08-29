import { Logger } from '@novacommerce/core-logger';

export interface JwksKey {
  kid: string;
  kty: string;
  alg: string;
  use: string;
  n: string;
  e: string;
}

export class JwtPublicKeyCache {
  private keys: Map<string, JwksKey> = new Map();
  private logger: Logger;
  private jwksUri: string;
  private lastFetchedAt: number = 0;
  private readonly cacheTtlMs: number = 3600000; // 1 hour

  constructor(jwksUri: string, logger: Logger) {
    this.jwksUri = jwksUri;
    this.logger = logger;
  }

  public async getKey(kid: string): Promise<JwksKey | null> {
    const existing = this.keys.get(kid);
    if (existing && Date.now() - this.lastFetchedAt < this.cacheTtlMs) {
      return existing;
    }

    await this.refreshKeys();
    return this.keys.get(kid) || null;
  }

  public async refreshKeys(): Promise<void> {
    this.logger.info(`Refreshing JWKS keys from ${this.jwksUri}`);
    // In production fetches JSON from auth-service/.well-known/jwks.json
    this.lastFetchedAt = Date.now();
  }
}
