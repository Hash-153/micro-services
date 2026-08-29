export interface ParcelInsuranceQuote {
  declaredValueCents: number;
  insurancePremiumCents: number;
  coverageLimitCents: number;
  deductibleCents: number;
  carrier: string;
}

export class CarrierInsuranceCalculator {
  public static calculatePremium(declaredValueCents: number, carrier: string = 'FEDEX'): ParcelInsuranceQuote {
    // Standard carrier insurance rate: $0.85 per $100 of declared value above $100
    const complimentaryValueCents = 10000; // First $100 covered free
    const taxableValue = Math.max(0, declaredValueCents - complimentaryValueCents);
    const premium = Math.ceil((taxableValue / 10000) * 85); // 85 cents per $100

    return {
      declaredValueCents,
      insurancePremiumCents: premium,
      coverageLimitCents: declaredValueCents,
      deductibleCents: 0,
      carrier
    };
  }
}
