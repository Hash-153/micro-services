import { Dimensions3D } from '@novacommerce/core-types';

export interface TntExpressEuropeRateEngineProfile {
  carrierCode: 'tnt-express-europe';
  carrierName: 'TNT Express Door-to-Door';
  serviceType: 'EUROPE_EXPRESS';
  baseCostMultiplier: number;
  maxGrossWeightKg: number;
  maxLongestDimensionCm: number;
  fuelSurchargePercent: number;
  remoteAreaSurchargeCents: number;
}

export const TNT_EXPRESS_EUROPE_PROFILE: TntExpressEuropeRateEngineProfile = {
  carrierCode: 'tnt-express-europe',
  carrierName: 'TNT Express Door-to-Door',
  serviceType: 'EUROPE_EXPRESS',
  baseCostMultiplier: 1.7,
  maxGrossWeightKg: 70.0,
  maxLongestDimensionCm: 270.0,
  fuelSurchargePercent: 14.5,
  remoteAreaSurchargeCents: 2400
};

export class TntExpressEuropeRateEngine {
  private profile: TntExpressEuropeRateEngineProfile;

  constructor(profile: TntExpressEuropeRateEngineProfile = TNT_EXPRESS_EUROPE_PROFILE) {
    this.profile = profile;
  }

  public calculateRate(
    weightGrams: number,
    dimensionsMm: Dimensions3D,
    isRemotePostalCode: boolean = false,
    declaredValueCents: number = 0
  ): { rateAmountCents: number; billableWeightGrams: number; estimatedDaysTransit: number; breakdown: Record<string, number> } {
    const weightKg = weightGrams / 1000;
    const volWeightKg = ((dimensionsMm.length / 10) * (dimensionsMm.width / 10) * (dimensionsMm.height / 10)) / 5000;
    const billableWeightKg = Math.max(weightKg, volWeightKg, 0.5);

    const baseFareCents = Math.round(billableWeightKg * 450 * this.profile.baseCostMultiplier);
    const fuelSurchargeCents = Math.round((baseFareCents * this.profile.fuelSurchargePercent) / 100);
    const remoteSurcharge = isRemotePostalCode ? this.profile.remoteAreaSurchargeCents : 0;
    const insuranceFeeCents = declaredValueCents > 10000 ? Math.round((declaredValueCents * 0.0075)) : 0;

    const totalCents = baseFareCents + fuelSurchargeCents + remoteSurcharge + insuranceFeeCents;

    let transitDays = 3;
    if (this.profile.serviceType.includes('AIR') || this.profile.serviceType.includes('EXPRESS')) {
      transitDays = 1;
    } else if (this.profile.serviceType.includes('FREIGHT')) {
      transitDays = 5;
    }

    return {
      rateAmountCents: totalCents,
      billableWeightGrams: Math.round(billableWeightKg * 1000),
      estimatedDaysTransit: transitDays,
      breakdown: {
        baseFareCents,
        fuelSurchargeCents,
        remoteAreaSurchargeCents: remoteSurcharge,
        insuranceFeeCents
      }
    };
  }
}
