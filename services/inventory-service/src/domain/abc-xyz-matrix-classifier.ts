export type AbcXyzClass = 'AX' | 'AY' | 'AZ' | 'BX' | 'BY' | 'BZ' | 'CX' | 'CY' | 'CZ';

export interface SkuDemandHistory {
  sku: string;
  monthlyDemandUnits: number[];
  unitCostCents: number;
}

export class AbcXyzMatrixClassifier {
  public static classify(history: SkuDemandHistory, abcClass: 'A' | 'B' | 'C'): { matrixClass: AbcXyzClass; coefficientOfVariation: number; demandPredictability: 'HIGH' | 'MEDIUM' | 'VOLATILE' } {
    const demand = history.monthlyDemandUnits;
    if (demand.length === 0) {
      return { matrixClass: `${abcClass}Z` as AbcXyzClass, coefficientOfVariation: 1.0, demandPredictability: 'VOLATILE' };
    }

    const mean = demand.reduce((a, b) => a + b, 0) / demand.length;
    const variance = demand.reduce((acc, v) => acc + Math.pow(v - mean, 2), 0) / demand.length;
    const stdDev = Math.sqrt(variance);

    const cv = mean > 0 ? stdDev / mean : 1.0;

    let xyz: 'X' | 'Y' | 'Z' = 'Z';
    let predictability: 'HIGH' | 'MEDIUM' | 'VOLATILE' = 'VOLATILE';

    if (cv <= 0.25) {
      xyz = 'X';
      predictability = 'HIGH';
    } else if (cv <= 0.60) {
      xyz = 'Y';
      predictability = 'MEDIUM';
    }

    return {
      matrixClass: `${abcClass}${xyz}` as AbcXyzClass,
      coefficientOfVariation: Math.round(cv * 100) / 100,
      demandPredictability: predictability
    };
  }
}
