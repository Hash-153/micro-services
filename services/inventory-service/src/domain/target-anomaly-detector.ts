export class TargetAnomalyDetector {
  public static detectSpike(currentSafetyStock: number, newCalculatedSafetyStock: number, maxAllowedRatio: number = 3.0): { isAnomaly: boolean; ratio: number; alertMessage?: string } {
    if (currentSafetyStock <= 0) return { isAnomaly: false, ratio: 1.0 };

    const ratio = newCalculatedSafetyStock / currentSafetyStock;
    if (ratio >= maxAllowedRatio) {
      return {
        isAnomaly: true,
        ratio: Math.round(ratio * 10) / 10,
        alertMessage: `Safety stock sudden spike detected: proposed (${newCalculatedSafetyStock}) is ${(ratio).toFixed(1)}x current baseline (${currentSafetyStock})`
      };
    }

    return { isAnomaly: false, ratio: Math.round(ratio * 10) / 10 };
  }
}
