import { FacilityTransferPlanItem } from './target-balancing-plan-exporter.js';

export class TargetBalancingPlanAuditLogger {
  public static logExecution(plan: FacilityTransferPlanItem[], executedByUserId: string): string {
    const timestamp = new Date().toISOString();
    return `[${timestamp}] User '${executedByUserId}' executed balancing plan with ${plan.length} inter-facility inventory movements.`;
  }
}
