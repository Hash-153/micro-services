export interface Level3QualificationCheck {
  isQualified: boolean;
  missingRequirements: string[];
  estimatedInterchangeSavingsBps: number;
}

export class MerchantLevel3Qualifier {
  public static evaluateQualification(
    hasCustomerVat: boolean,
    hasLineItemCommodityCodes: boolean,
    hasFreightAmount: boolean,
    hasTaxAmount: boolean
  ): Level3QualificationCheck {
    const missing: string[] = [];

    if (!hasLineItemCommodityCodes) missing.push('Line item UNSPSC commodity codes required');
    if (!hasCustomerVat) missing.push('Customer VAT / Tax Registration Number required');
    if (!hasFreightAmount) missing.push('Explicit freight breakout amount required');
    if (!hasTaxAmount) missing.push('Explicit tax calculation amount required');

    const isQualified = missing.length === 0;

    return {
      isQualified,
      missingRequirements: missing,
      estimatedInterchangeSavingsBps: isQualified ? 80 : 0 // 0.80% interchange savings on commercial cards
    };
  }
}
