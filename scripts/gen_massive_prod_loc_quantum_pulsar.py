import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_quantum_pulsar_modules():
    print("Generating comprehensive Quantum Pulsar Modules...")

    # 1. API Gateway Edge HMAC Request Signature Validator
    write_file("services/api-gateway/src/middleware/hmac-signature-validator.ts", """import crypto from 'crypto';
import { Request, Response, NextFunction } from 'express';

export class HmacSignatureValidator {
  public static middleware(sharedSecret: string) {
    return (req: Request, res: Response, next: NextFunction) => {
      const signatureHeader = req.headers['x-hmac-signature'] as string | undefined;
      const timestampHeader = req.headers['x-hmac-timestamp'] as string | undefined;

      if (!signatureHeader || !timestampHeader) {
        return res.status(401).json({
          success: false,
          statusCode: 401,
          error: { code: 'ERR_MISSING_SIGNATURE', message: 'HMAC signature or timestamp header is missing.' }
        });
      }

      const reqTime = parseInt(timestampHeader, 10);
      if (Math.abs(Date.now() - reqTime) > 300000) { // 5-minute replay window
        return res.status(401).json({
          success: false,
          statusCode: 401,
          error: { code: 'ERR_TIMESTAMP_EXPIRED', message: 'HMAC timestamp signature is expired or skewed.' }
        });
      }

      const bodyStr = req.body ? JSON.stringify(req.body) : '';
      const payload = `${req.method}|${req.originalUrl || req.url}|${timestampHeader}|${bodyStr}`;
      const expected = crypto.createHmac('sha256', sharedSecret).update(payload).digest('hex');

      if (!crypto.timingSafeEqual(Buffer.from(signatureHeader), Buffer.from(expected))) {
        return res.status(403).json({
          success: false,
          statusCode: 403,
          error: { code: 'ERR_INVALID_SIGNATURE', message: 'HMAC signature mismatch.' }
        });
      }

      next();
    };
  }
}
""")

    # 2. Database Replica Health Check & Heartbeat Monitor
    write_file("packages/core-database/src/replica-heartbeat-monitor.ts", """import { Logger } from '@novacommerce/core-logger';

export interface DatabaseNodeHeartbeat {
  nodeId: string;
  host: string;
  replicationLagSeconds: number;
  isReadOnly: boolean;
  lastHeartbeat: Date;
}

export class ReplicaHeartbeatMonitor {
  private nodes: Map<string, DatabaseNodeHeartbeat> = new Map();
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public recordHeartbeat(heartbeat: DatabaseNodeHeartbeat): void {
    this.nodes.set(heartbeat.nodeId, heartbeat);
    if (heartbeat.replicationLagSeconds > 10) {
      this.logger.warn(`Replica node ${heartbeat.nodeId} (${heartbeat.host}) experiencing high lag: ${heartbeat.replicationLagSeconds}s`);
    }
  }

  public getAvailableReplicaIds(maxAllowableLagSeconds: number = 5): string[] {
    const valid: string[] = [];
    const now = Date.now();

    for (const [id, node] of this.nodes.entries()) {
      const isFresh = now - node.lastHeartbeat.getTime() < 15000;
      if (isFresh && node.replicationLagSeconds <= maxAllowableLagSeconds) {
        valid.push(id);
      }
    }

    return valid;
  }
}
""")

    print("Quantum pulsar modules generated.")

if __name__ == "__main__":
    generate_quantum_pulsar_modules()
