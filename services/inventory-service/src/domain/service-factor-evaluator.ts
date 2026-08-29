export class ServiceFactorEvaluator {
  private static readonly SERVICE_LEVEL_Z_TABLE: { targetPercent: number; zScore: number }[] = [
    { targetPercent: 90.0, zScore: 1.28 },
    { targetPercent: 95.0, zScore: 1.65 },
    { targetPercent: 98.0, zScore: 2.05 },
    { targetPercent: 99.0, zScore: 2.33 },
    { targetPercent: 99.5, zScore: 2.58 },
    { targetPercent: 99.9, zScore: 3.09 }
  ];

  public static getZScore(targetServiceLevelPercent: number): number {
    const match = this.SERVICE_LEVEL_Z_TABLE.find(t => t.targetPercent >= targetServiceLevelPercent);
    return match ? match.zScore : 1.65; // Default 95%
  }
}
