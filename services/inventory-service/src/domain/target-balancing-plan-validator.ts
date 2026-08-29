import { FacilityTransferPlanItem } from './target-balancing-plan-exporter.js';

export class TargetBalancingPlanValidator {
  public static validatePlan(plan: FacilityTransferPlanItem[]): { isValid: boolean; invalidTransfersCount: number; errors: string[] } {
    const errors: string[] = [];
    let invalidCount = 0;

    for (const item of plan) {
      if (item.sourceFacilityId === item.targetFacilityId) {
        errors.push(`Invalid transfer: source and target facility are identical (${item.sourceFacilityId})`);
        invalidCount++;
      }
      if (item.transferQuantity <= 0) {
        errors.push(`Invalid transfer quantity (${item.transferQuantity}) for SKU ${item.sku}`);
        invalidCount++;
      }
    }

    return {
      isValid: invalidCount === 0,
      invalidTransfersCount: invalidCount,
      errors
    };
  }
}
