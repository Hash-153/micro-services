export interface FacilityTransferPlanItem {
  sourceFacilityId: string;
  targetFacilityId: string;
  sku: string;
  transferQuantity: number;
}

export class TargetBalancingPlanExporter {
  public static exportPlanJson(plan: FacilityTransferPlanItem[]): string {
    return JSON.stringify({
      generatedAt: new Date().toISOString(),
      totalTransfers: plan.length,
      plan
    }, null, 2);
  }
}
