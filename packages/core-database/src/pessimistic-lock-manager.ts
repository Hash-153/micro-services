import { Logger } from '@novacommerce/core-logger';

export class PessimisticLockManager {
  private logger: Logger;
  private lockedResources: Map<string, { lockHolderId: string; expiresAt: number }> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async acquireLock(resourceKey: string, lockHolderId: string, ttlMs: number = 5000): Promise<boolean> {
    const now = Date.now();
    const existing = this.lockedResources.get(resourceKey);

    if (existing && existing.expiresAt > now && existing.lockHolderId !== lockHolderId) {
      return false; // Resource locked by another transaction
    }

    this.lockedResources.set(resourceKey, {
      lockHolderId,
      expiresAt: now + ttlMs
    });

    this.logger.info(`Pessimistic lock acquired on '${resourceKey}' by holder '${lockHolderId}' (ttl=${ttlMs}ms)`);
    return true;
  }

  public async releaseLock(resourceKey: string, lockHolderId: string): Promise<boolean> {
    const existing = this.lockedResources.get(resourceKey);
    if (!existing || existing.lockHolderId !== lockHolderId) {
      return false;
    }

    this.lockedResources.delete(resourceKey);
    this.logger.info(`Pessimistic lock released on '${resourceKey}' by holder '${lockHolderId}'`);
    return true;
  }
}
