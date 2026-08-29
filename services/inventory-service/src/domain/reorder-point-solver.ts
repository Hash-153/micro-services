export interface SkuVelocityProfile {
  sku: string;
  leadTimeDays: number;
  averageDailySales: number;
  maxDailySales: number;
  maxLeadTimeDays: number;
}

export class ReorderPointSolver {
  public static computeReorderPoint(profile: SkuVelocityProfile): { reorderPoint: number; safetyStock: number; leadTimeDemand: number } {
    const maxUsage = profile.maxDailySales * profile.maxLeadTimeDays;
    const avgUsage = profile.averageDailySales * profile.leadTimeDays;
    const safetyStock = Math.max(0, maxUsage - avgUsage);
    const leadTimeDemand = Math.round(avgUsage);
    const reorderPoint = leadTimeDemand + Math.round(safetyStock);

    return {
      reorderPoint,
      safetyStock: Math.round(safetyStock),
      leadTimeDemand
    };
  }
}
