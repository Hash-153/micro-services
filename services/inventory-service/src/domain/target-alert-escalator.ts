export class TargetAlertEscalator {
  public static determineEscalationTier(skusBelowSafetyStockCount: number, criticalSkusCount: number): 'TIER_1_AUTO' | 'TIER_2_SUPERVISOR' | 'TIER_3_EXECUTIVE_OPS' {
    if (criticalSkusCount >= 5 || skusBelowSafetyStockCount >= 50) {
      return 'TIER_3_EXECUTIVE_OPS';
    }
    if (criticalSkusCount >= 1 || skusBelowSafetyStockCount >= 15) {
      return 'TIER_2_SUPERVISOR';
    }
    return 'TIER_1_AUTO';
  }
}
