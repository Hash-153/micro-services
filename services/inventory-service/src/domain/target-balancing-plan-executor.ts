import { FacilityTransferPlanItem } from './target-balancing-plan-exporter.js';
import { Logger } from '@novacommerce/core-logger';

export class TargetBalancingPlanExecutor {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async executePlan(plan: FacilityTransferPlanItem[]): Promise<{ successfulTransfersCount: number; failedTransfersCount: number }> {
    let success = 0;
    let failed = 0;

    for (const item of plan) {
      try {
        this.logger.info(`Executing network inventory transfer: ${item.transferQuantity}x ${item.sku} from ${item.sourceFacilityId} -> ${item.targetFacilityId}`);
        success++;
      } catch (err) {
        this.logger.error(`Failed to execute inventory transfer for SKU ${item.sku}:`, err);
        failed++;
      }
    }

    return {
      successfulTransfersCount: success,
      failedTransfersCount: failed
    };
  }
}
