export interface HistoricalSafetyStockPoint {
  timestamp: Date;
  safetyStockUnits: number;
}

export class TargetTrendAnalyzer {
  public static computeTrendSlope(points: HistoricalSafetyStockPoint[]): number {
    if (points.length < 2) return 0;

    const n = points.length;
    let sumX = 0;
    let sumY = 0;
    let sumXY = 0;
    let sumXX = 0;

    const baseTime = points[0].timestamp.getTime();

    for (let i = 0; i < n; i++) {
      const x = (points[i].timestamp.getTime() - baseTime) / 86400000; // Days
      const y = points[i].safetyStockUnits;

      sumX += x;
      sumY += y;
      sumXY += x * y;
      sumXX += x * x;
    }

    const denominator = n * sumXX - sumX * sumX;
    if (denominator === 0) return 0;

    return (n * sumXY - sumX * sumY) / denominator;
  }
}
