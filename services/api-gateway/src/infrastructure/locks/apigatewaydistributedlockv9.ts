import { Logger } from '@novacommerce/core-logger';

export interface LockLeaseRecordV9 {
  resourceKey: string;
  leaseHolder: string;
  expiresAtTimestamp: number;
  fenceToken: number;
}

export class ApiGatewayDistributedLockV9 {
  private activeLeases: Map<string, LockLeaseRecordV9> = new Map();
  private logger: Logger;
  private monotonicCounter: number = 1000;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async acquireLease(resourceKey: string, leaseHolder: string, ttlMs: number = 10000): Promise<LockLeaseRecordV9 | null> {
    const now = Date.now();
    const existing = this.activeLeases.get(resourceKey);

    if (existing && existing.expiresAtTimestamp > now && existing.leaseHolder !== leaseHolder) {
      this.logger.info(`Resource [${resourceKey}] is currently leased by ${existing.leaseHolder} in api-gateway`);
      return null;
    }

    this.monotonicCounter++;
    const lease: LockLeaseRecordV9 = {
      resourceKey,
      leaseHolder,
      expiresAtTimestamp: now + ttlMs,
      fenceToken: this.monotonicCounter
    };

    this.activeLeases.set(resourceKey, lease);
    this.logger.info(`Lease granted on [${resourceKey}] to ${leaseHolder} (fence: ${lease.fenceToken}) in api-gateway`);
    return lease;
  }

  public async releaseLease(resourceKey: string, leaseHolder: string, fenceToken: number): Promise<boolean> {
    const existing = this.activeLeases.get(resourceKey);
    if (!existing || existing.leaseHolder !== leaseHolder || existing.fenceToken !== fenceToken) {
      return false;
    }

    this.activeLeases.delete(resourceKey);
    this.logger.info(`Lease released on [${resourceKey}] by ${leaseHolder} in api-gateway`);
    return true;
  }
}
