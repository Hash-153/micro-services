import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v28():
    print("Generating comprehensive Production V28 Modules...")

    # 1. API Gateway Edge Payload Decryption Middleware (JWE / AES-GCM)
    write_file("services/api-gateway/src/middleware/payload-decryption.ts", """import crypto from 'crypto';
import { Request, Response, NextFunction } from 'express';

export class PayloadDecryptionMiddleware {
  public static middleware(aesKeyBase64: string) {
    const key = Buffer.from(aesKeyBase64, 'base64');

    return (req: Request, res: Response, next: NextFunction) => {
      const isEncrypted = req.headers['x-payload-encryption'] === 'AES-256-GCM';
      if (!isEncrypted || !req.body?.encryptedData) {
        return next();
      }

      try {
        const { encryptedData, iv, authTag } = req.body;
        const decipher = crypto.createDecipheriv('aes-256-gcm', key, Buffer.from(iv, 'base64'));
        decipher.setAuthTag(Buffer.from(authTag, 'base64'));

        let decrypted = decipher.update(encryptedData, 'base64', 'utf8');
        decrypted += decipher.final('utf8');

        req.body = JSON.parse(decrypted);
        next();
      } catch (err) {
        return res.status(400).json({
          success: false,
          statusCode: 400,
          error: { code: 'ERR_DECRYPTION_FAILED', message: 'Failed to decrypt secure payload.' }
        });
      }
    };
  }
}
""")

    # 2. User Service Multi-Tenant Data Isolation Guard
    write_file("services/user-service/src/domain/tenant-isolation-guard.ts", """export class TenantIsolationGuard {
  public static enforceOrgAccess(requestedOrgId: string, userOrgId?: string, isSuperAdmin: boolean = false): void {
    if (isSuperAdmin) return; // Super admins have global access

    if (!userOrgId || userOrgId !== requestedOrgId) {
      throw new Error(`Tenant access violation: user in organization '${userOrgId || 'NONE'}' cannot access resources in organization '${requestedOrgId}'`);
    }
  }
}
""")

    print("Production V28 modules generated.")

if __name__ == "__main__":
    generate_prod_v28()
