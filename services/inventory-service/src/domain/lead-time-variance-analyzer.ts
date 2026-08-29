export interface SupplierDeliveryRecord {
  poNumber: string;
  expectedDate: Date;
  actualReceiptDate: Date;
  varianceDays: number;
}

export class LeadTimeVarianceAnalyzer {
  public static computeVariance(records: SupplierDeliveryRecord[]): { meanVarianceDays: number; standardDeviationDays: number; isUnreliable: boolean } {
    if (records.length === 0) return { meanVarianceDays: 0, standardDeviationDays: 0, isUnreliable: false };

    const variances = records.map(r => (r.actualReceiptDate.getTime() - r.expectedDate.getTime()) / 86400000);
    const mean = variances.reduce((a, b) => a + b, 0) / variances.length;
    const variance = variances.reduce((acc, v) => acc + Math.pow(v - mean, 2), 0) / variances.length;
    const stdDev = Math.sqrt(variance);

    return {
      meanVarianceDays: Math.round(mean * 10) / 10,
      standardDeviationDays: Math.round(stdDev * 10) / 10,
      isUnreliable: mean > 5 || stdDev > 3
    };
  }
}
