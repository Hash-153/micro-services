export interface BinCountComparison {
  binId: string;
  sku: string;
  systemQuantity: number;
  physicalCountQuantity: number;
  unitCostCents: number;
}

export class CycleCountDiscrepancyAnalyzer {
  public static analyzeDiscrepancy(item: BinCountComparison): {
    varianceUnits: number;
    varianceCents: number;
    variancePercentage: number;
    severity: 'NORMAL' | 'WARNING' | 'CRITICAL';
    requiresSupervisorApproval: boolean;
  } {
    const varianceUnits = item.physicalCountQuantity - item.systemQuantity;
    const varianceCents = varianceUnits * item.unitCostCents;
    const variancePercentage = item.systemQuantity > 0
      ? (Math.abs(varianceUnits) / item.systemQuantity) * 100
      : (item.physicalCountQuantity > 0 ? 100 : 0);

    let severity: 'NORMAL' | 'WARNING' | 'CRITICAL' = 'NORMAL';
    if (Math.abs(varianceCents) >= 50000 || variancePercentage >= 20) {
      severity = 'CRITICAL';
    } else if (Math.abs(varianceCents) >= 10000 || variancePercentage >= 5) {
      severity = 'WARNING';
    }

    return {
      varianceUnits,
      varianceCents,
      variancePercentage: Math.round(variancePercentage * 10) / 10,
      severity,
      requiresSupervisorApproval: severity === 'CRITICAL'
    };
  }
}
