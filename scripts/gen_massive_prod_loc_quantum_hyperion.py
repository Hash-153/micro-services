import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_quantum_hyperion_modules():
    print("Generating comprehensive Quantum Hyperion Modules...")

    # 1. API Gateway Distributed Request Deduplication Nonce Cache
    write_file("services/api-gateway/src/middleware/nonce-cache.ts", """import { Request, Response, NextFunction } from 'express';

export class NonceCacheMiddleware {
  private static nonces: Map<string, number> = new Map(); // nonce -> expiry timestamp

  public static middleware(ttlSeconds: number = 300) {
    return (req: Request, res: Response, next: NextFunction) => {
      const nonce = req.headers['x-request-nonce'] as string | undefined;
      if (!nonce) {
        return next(); // Nonce not required for all endpoints
      }

      const now = Date.now();
      const existing = this.nonces.get(nonce);

      if (existing && existing > now) {
        return res.status(409).json({
          success: false,
          statusCode: 409,
          error: { code: 'ERR_DUPLICATE_NONCE', message: 'Request nonce has already been consumed.' }
        });
      }

      this.nonces.set(nonce, now + ttlSeconds * 1000);
      next();
    };
  }
}
""")

    # 2. Database Read-Write Splitting Connection Proxy
    write_file("packages/core-database/src/rw-split-proxy.ts", """import { DatabaseClient } from './index.js';
import { Logger } from '@novacommerce/core-logger';

export class ReadWriteSplitProxy {
  private primaryDb: DatabaseClient;
  private replicaDbs: DatabaseClient[];
  private logger: Logger;
  private rrIndex: number = 0;

  constructor(primaryDb: DatabaseClient, replicaDbs: DatabaseClient[], logger: Logger) {
    this.primaryDb = primaryDb;
    this.replicaDbs = replicaDbs;
    this.logger = logger;
  }

  public async query<T = any>(sql: string, params: any[] = []): Promise<T[]> {
    const trimmed = sql.trim().toUpperCase();
    const isReadOnly = trimmed.startsWith('SELECT') && !trimmed.includes('FOR UPDATE');

    if (isReadOnly && this.replicaDbs.length > 0) {
      const replica = this.replicaDbs[this.rrIndex % this.replicaDbs.length];
      this.rrIndex++;
      try {
        return await replica.query<T>(sql, params);
      } catch (err) {
        this.logger.warn('Replica read failed, falling back to primary database');
      }
    }

    return await this.primaryDb.query<T>(sql, params);
  }
}
""")

    print("Quantum hyperion modules generated.")

if __name__ == "__main__":
    generate_quantum_hyperion_modules()
