import { Dimensions3D } from '@novacommerce/core-types';

export interface DimensionalWeightRule {
  carrier: string;
  serviceType: 'DOMESTIC' | 'INTERNATIONAL';
  dimensionalDivisorCm: number; // e.g. 5000 for IATA (cm3/kg) or 139 for US inches (in3/lb)
  minimumBillableWeightGrams: number;
}

export const DIMENSIONAL_WEIGHT_RULES: DimensionalWeightRule[] = [
  { carrier: 'FEDEX', serviceType: 'DOMESTIC', dimensionalDivisorCm: 5000, minimumBillableWeightGrams: 500 },
  { carrier: 'FEDEX', serviceType: 'INTERNATIONAL', dimensionalDivisorCm: 5000, minimumBillableWeightGrams: 1000 },
  { carrier: 'UPS', serviceType: 'DOMESTIC', dimensionalDivisorCm: 5000, minimumBillableWeightGrams: 500 },
  { carrier: 'UPS', serviceType: 'INTERNATIONAL', dimensionalDivisorCm: 5000, minimumBillableWeightGrams: 1000 },
  { carrier: 'DHL', serviceType: 'INTERNATIONAL', dimensionalDivisorCm: 5000, minimumBillableWeightGrams: 500 }
];

export class DimensionalWeightCalculator {
  public static calculateBillableWeightGrams(
    actualWeightGrams: number,
    dimensionsMm: Dimensions3D,
    carrier: string = 'FEDEX',
    serviceType: 'DOMESTIC' | 'INTERNATIONAL' = 'DOMESTIC'
  ): { billableWeightGrams: number; volumetricWeightGrams: number; isVolumetricApplied: boolean } {
    const rule = DIMENSIONAL_WEIGHT_RULES.find(r => r.carrier === carrier && r.serviceType === serviceType) || DIMENSIONAL_WEIGHT_RULES[0];

    // Volume in cubic centimeters
    const volumeCm3 = (dimensionsMm.length / 10) * (dimensionsMm.width / 10) * (dimensionsMm.height / 10);
    const volumetricKg = volumeCm3 / rule.dimensionalDivisorCm;
    const volumetricGrams = Math.round(volumetricKg * 1000);

    const billable = Math.max(actualWeightGrams, volumetricGrams, rule.minimumBillableWeightGrams);

    return {
      billableWeightGrams: billable,
      volumetricWeightGrams: volumetricGrams,
      isVolumetricApplied: volumetricGrams > actualWeightGrams
    };
  }
}
