export interface AbcReorderPolicy {
  classification: 'A' | 'B' | 'C';
  reviewCycleDays: number;
  serviceLevelTargetPercent: number;
  safetyStockDaysOfSupply: number;
  maxStockDaysOfSupply: number;
  minOrderQuantityUnits: number;
}

export const ABC_REORDER_POLICIES: Record<'A' | 'B' | 'C', AbcReorderPolicy> = {
  A: {
    classification: 'A',
    reviewCycleDays: 7, // Reviewed weekly
    serviceLevelTargetPercent: 99.5,
    safetyStockDaysOfSupply: 14,
    maxStockDaysOfSupply: 45,
    minOrderQuantityUnits: 10
  },
  B: {
    classification: 'B',
    reviewCycleDays: 30, // Reviewed monthly
    serviceLevelTargetPercent: 95.0,
    safetyStockDaysOfSupply: 30,
    maxStockDaysOfSupply: 90,
    minOrderQuantityUnits: 25
  },
  C: {
    classification: 'C',
    reviewCycleDays: 90, // Reviewed quarterly
    serviceLevelTargetPercent: 90.0,
    safetyStockDaysOfSupply: 60,
    maxStockDaysOfSupply: 180,
    minOrderQuantityUnits: 50
  }
};

export class AbcPolicyEvaluator {
  public static getPolicy(classification: 'A' | 'B' | 'C'): AbcReorderPolicy {
    return ABC_REORDER_POLICIES[classification] || ABC_REORDER_POLICIES.B;
  }
}
