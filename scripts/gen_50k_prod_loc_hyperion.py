import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_hyperion():
    print("Generating comprehensive Production Hyperion Modules...")

    # 1. API Gateway Response Cache Middleware
    write_file("services/api-gateway/src/middleware/response-cache.middleware.ts", """import { Request, Response, NextFunction } from 'express';
import { Logger } from '@novacommerce/core-logger';

export class ResponseCacheMiddleware {
  private cache: Map<string, { body: any; headers: Record<string, any>; expiresAt: number }> = new Map();
  private logger: Logger;
  private defaultTtlSeconds: number;

  constructor(logger: Logger, defaultTtlSeconds: number = 60) {
    this.logger = logger;
    this.defaultTtlSeconds = defaultTtlSeconds;
  }

  public middleware() {
    return (req: Request, res: Response, next: NextFunction) => {
      if (req.method !== 'GET') {
        return next();
      }

      const cacheKey = `${req.originalUrl || req.url}`;
      const cached = this.cache.get(cacheKey);

      if (cached && Date.now() < cached.expiresAt) {
        res.setHeader('X-Cache-Status', 'HIT');
        return res.json(cached.body);
      }

      res.setHeader('X-Cache-Status', 'MISS');
      const originalJson = res.json.bind(res);

      res.json = (body: any) => {
        if (res.statusCode === 200) {
          this.cache.set(cacheKey, {
            body,
            headers: {},
            expiresAt: Date.now() + this.defaultTtlSeconds * 1000
          });
        }
        return originalJson(body);
      };

      next();
    };
  }

  public clear(): void {
    this.cache.clear();
  }
}
""")

    # 2. Database Read Replica Load Balancer
    write_file("packages/core-database/src/replica-load-balancer.ts", """import { Logger } from '@novacommerce/core-logger';

export interface DatabaseNode {
  nodeId: string;
  host: string;
  port: number;
  isMaster: boolean;
  weight: number;
  activeConnections: number;
}

export class ReplicaLoadBalancer {
  private logger: Logger;
  private nodes: DatabaseNode[] = [];
  private roundRobinIndex: number = 0;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public registerNode(node: DatabaseNode): void {
    this.nodes.push(node);
    this.logger.info(`Database node registered: ${node.nodeId} (${node.host}:${node.port}, isMaster=${node.isMaster})`);
  }

  public getMaster(): DatabaseNode {
    const master = this.nodes.find(n => n.isMaster);
    if (!master) throw new Error('No master database node registered');
    return master;
  }

  public getReadReplica(): DatabaseNode {
    const replicas = this.nodes.filter(n => !n.isMaster);
    if (replicas.length === 0) {
      return this.getMaster(); // Fallback to master
    }

    const selected = replicas[this.roundRobinIndex % replicas.length];
    this.roundRobinIndex++;
    return selected;
  }
}
""")

    print("Production hyperion modules generated.")

if __name__ == "__main__":
    generate_prod_hyperion()
