import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v31():
    print("Generating comprehensive Production V31 Modules...")

    # 1. API Gateway Edge DDoS Mitigation & Syn Flood Guard
    write_file("services/api-gateway/src/middleware/ddos-mitigation.ts", """import { Request, Response, NextFunction } from 'express';
import { Logger } from '@novacommerce/core-logger';

export class DdosMitigationGuard {
  private ipConnections: Map<string, number> = new Map();
  private maxConcurrentPerIp: number;
  private logger: Logger;

  constructor(logger: Logger, maxConcurrentPerIp: number = 50) {
    this.logger = logger;
    this.maxConcurrentPerIp = maxConcurrentPerIp;
  }

  public middleware() {
    return (req: Request, res: Response, next: NextFunction) => {
      const ip = req.ip || req.socket.remoteAddress || '127.0.0.1';
      const current = this.ipConnections.get(ip) || 0;

      if (current >= this.maxConcurrentPerIp) {
        this.logger.warn(`DDoS mitigation: dropped concurrent connection flood from IP ${ip} (${current} active)`);
        return res.status(429).json({
          success: false,
          statusCode: 429,
          error: { code: 'ERR_CONCURRENT_LIMIT_EXCEEDED', message: 'Too many concurrent socket connections from this IP.' }
        });
      }

      this.ipConnections.set(ip, current + 1);

      res.on('finish', () => {
        const count = this.ipConnections.get(ip) || 1;
        if (count <= 1) {
          this.ipConnections.delete(ip);
        } else {
          this.ipConnections.set(ip, count - 1);
        }
      });

      next();
    };
  }
}
""")

    # 2. User Service GDPR Right to be Forgotten Eraser
    write_file("services/user-service/src/domain/gdpr-eraser.ts", """import { UserProfileEntity, AddressEntity } from '@novacommerce/core-types';

export class GdprErasureEngine {
  public static anonymizeProfile(profile: UserProfileEntity): UserProfileEntity {
    const anonymousId = `anon_${Date.now().toString(36)}`;

    return {
      ...profile,
      firstName: 'ANONYMIZED',
      lastName: 'ANONYMIZED',
      avatarUrl: undefined,
      timezone: 'UTC',
      updatedAt: new Date()
    };
  }

  public static anonymizeAddress(address: AddressEntity): AddressEntity {
    return {
      ...address,
      recipientName: 'REDACTED GDPR',
      streetLine1: 'REDACTED GDPR',
      streetLine2: undefined,
      phone: undefined,
      updatedAt: new Date()
    };
  }
}
""")

    print("Production V31 modules generated.")

if __name__ == "__main__":
    generate_prod_v31()
