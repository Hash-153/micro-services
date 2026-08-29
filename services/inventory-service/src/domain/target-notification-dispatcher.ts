import { Logger } from '@novacommerce/core-logger';

export class TargetNotificationDispatcher {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async notifyReplenishmentThresholdBreached(sku: string, currentStock: number, safetyStock: number): Promise<void> {
    this.logger.warn(`Replenishment alert: SKU '${sku}' on-hand stock (${currentStock}) dropped below safety stock (${safetyStock})`);
  }
}
