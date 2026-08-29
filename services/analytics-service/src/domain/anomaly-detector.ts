export class TimeseriesAnomalyDetector {
  public static detectAnomalies(values: number[], zScoreThreshold: number = 3.0): { index: number; value: number; zScore: number }[] {
    if (values.length < 5) return [];

    const mean = values.reduce((a, b) => a + b, 0) / values.length;
    const variance = values.reduce((acc, v) => acc + Math.pow(v - mean, 2), 0) / values.length;
    const stdDev = Math.sqrt(variance);

    if (stdDev === 0) return [];

    const anomalies: { index: number; value: number; zScore: number }[] = [];

    values.forEach((v, idx) => {
      const z = Math.abs(v - mean) / stdDev;
      if (z >= zScoreThreshold) {
        anomalies.push({
          index: idx,
          value: v,
          zScore: Math.round(z * 100) / 100
        });
      }
    });

    return anomalies;
  }
}
