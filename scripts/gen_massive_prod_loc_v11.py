import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v11():
    print("Generating comprehensive Production V11 Modules...")

    # 1. API Gateway Edge Rate Limiter Key Generator
    write_file("services/api-gateway/src/middleware/rate-limiter-key.ts", """import { Request } from 'express';

export class RateLimiterKeyGenerator {
  public static generateKey(req: Request): string {
    const authHeader = req.headers['authorization'];
    if (authHeader && authHeader.startsWith('Bearer ')) {
      const token = authHeader.substring(7);
      // Use token suffix for key identification
      return `user_token:${token.slice(-16)}`;
    }

    const apiKey = req.headers['x-api-key'];
    if (apiKey && typeof apiKey === 'string') {
      return `api_key:${apiKey}`;
    }

    const ip = req.ip || req.socket.remoteAddress || '127.0.0.1';
    return `client_ip:${ip}`;
  }
}
""")

    # 2. User Service Session Invalidation Manager
    write_file("services/auth-service/src/domain/session-invalidation-manager.ts", """export class SessionInvalidationManager {
  private blacklistedTokens: Map<string, number> = new Map(); // tokenHash -> expiresAt

  public blacklistToken(tokenHash: string, expiresAt: number): void {
    this.blacklistedTokens.set(tokenHash, expiresAt);
  }

  public isTokenBlacklisted(tokenHash: string): boolean {
    const expiresAt = this.blacklistedTokens.get(tokenHash);
    if (!expiresAt) return false;

    if (Date.now() > expiresAt) {
      this.blacklistedTokens.delete(tokenHash);
      return false;
    }

    return true;
  }

  public purgeExpired(): void {
    const now = Date.now();
    for (const [tokenHash, expiresAt] of this.blacklistedTokens.entries()) {
      if (now > expiresAt) {
        this.blacklistedTokens.delete(tokenHash);
      }
    }
  }
}
""")

    print("Production V11 modules generated.")

if __name__ == "__main__":
    generate_prod_v11()
