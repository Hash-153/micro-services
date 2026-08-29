import { SkuDemandDistribution, SafetyStockBufferCalculator } from './safety-stock-buffer-calculator.js';

export class TargetRecalibrator {
  public static recalibrateTargets(distributions: SkuDemandDistribution[]): { sku: string; targetUnits: number }[] {
    return distributions.map(d => ({
      sku: d.sku,
      targetUnits: SafetyStockBufferCalculator.calculateBuffer(d).safetyStockUnits
    }));
  }
}
