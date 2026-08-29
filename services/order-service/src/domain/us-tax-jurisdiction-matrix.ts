export interface StateTaxRateRecord {
  stateCode: string;
  stateName: string;
  stateBaseRatePercent: number;
  averageLocalRatePercent: number;
  combinedRatePercent: number;
  taxableServices: boolean;
  taxableShipping: boolean;
  economicNexusSalesThresholdCents: number;
  economicNexusTransactionThreshold: number;
}

export const US_STATE_TAX_MATRIX: Record<string, StateTaxRateRecord> = {
  AL: { stateCode: 'AL', stateName: 'Alabama', stateBaseRatePercent: 4.0, averageLocalRatePercent: 5.24, combinedRatePercent: 9.24, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 25000000, economicNexusTransactionThreshold: 0 },
  AK: { stateCode: 'AK', stateName: 'Alaska', stateBaseRatePercent: 0.0, averageLocalRatePercent: 1.76, combinedRatePercent: 1.76, taxableServices: false, taxableShipping: false, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  AZ: { stateCode: 'AZ', stateName: 'Arizona', stateBaseRatePercent: 5.6, averageLocalRatePercent: 2.77, combinedRatePercent: 8.37, taxableServices: true, taxableShipping: false, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 0 },
  AR: { stateCode: 'AR', stateName: 'Arkansas', stateBaseRatePercent: 6.5, averageLocalRatePercent: 2.93, combinedRatePercent: 9.43, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  CA: { stateCode: 'CA', stateName: 'California', stateBaseRatePercent: 7.25, averageLocalRatePercent: 1.57, combinedRatePercent: 8.82, taxableServices: false, taxableShipping: false, economicNexusSalesThresholdCents: 50000000, economicNexusTransactionThreshold: 0 },
  CO: { stateCode: 'CO', stateName: 'Colorado', stateBaseRatePercent: 2.9, averageLocalRatePercent: 4.87, combinedRatePercent: 7.77, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 0 },
  CT: { stateCode: 'CT', stateName: 'Connecticut', stateBaseRatePercent: 6.35, averageLocalRatePercent: 0.0, combinedRatePercent: 6.35, taxableServices: true, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  DE: { stateCode: 'DE', stateName: 'Delaware', stateBaseRatePercent: 0.0, averageLocalRatePercent: 0.0, combinedRatePercent: 0.0, taxableServices: false, taxableShipping: false, economicNexusSalesThresholdCents: 0, economicNexusTransactionThreshold: 0 },
  FL: { stateCode: 'FL', stateName: 'Florida', stateBaseRatePercent: 6.0, averageLocalRatePercent: 1.02, combinedRatePercent: 7.02, taxableServices: false, taxableShipping: false, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 0 },
  GA: { stateCode: 'GA', stateName: 'Georgia', stateBaseRatePercent: 4.0, averageLocalRatePercent: 3.35, combinedRatePercent: 7.35, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  HI: { stateCode: 'HI', stateName: 'Hawaii', stateBaseRatePercent: 4.0, averageLocalRatePercent: 0.44, combinedRatePercent: 4.44, taxableServices: true, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  ID: { stateCode: 'ID', stateName: 'Idaho', stateBaseRatePercent: 6.0, averageLocalRatePercent: 0.03, combinedRatePercent: 6.03, taxableServices: false, taxableShipping: false, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 0 },
  IL: { stateCode: 'IL', stateName: 'Illinois', stateBaseRatePercent: 6.25, averageLocalRatePercent: 2.56, combinedRatePercent: 8.81, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  IN: { stateCode: 'IN', stateName: 'Indiana', stateBaseRatePercent: 7.0, averageLocalRatePercent: 0.0, combinedRatePercent: 7.0, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  IA: { stateCode: 'IA', stateName: 'Iowa', stateBaseRatePercent: 6.0, averageLocalRatePercent: 0.94, combinedRatePercent: 6.94, taxableServices: true, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 0 },
  KS: { stateCode: 'KS', stateName: 'Kansas', stateBaseRatePercent: 6.5, averageLocalRatePercent: 2.19, combinedRatePercent: 8.69, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 0 },
  KY: { stateCode: 'KY', stateName: 'Kentucky', stateBaseRatePercent: 6.0, averageLocalRatePercent: 0.0, combinedRatePercent: 6.0, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  LA: { stateCode: 'LA', stateName: 'Louisiana', stateBaseRatePercent: 4.45, averageLocalRatePercent: 5.1, combinedRatePercent: 9.55, taxableServices: false, taxableShipping: false, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  ME: { stateCode: 'ME', stateName: 'Maine', stateBaseRatePercent: 5.5, averageLocalRatePercent: 0.0, combinedRatePercent: 5.5, taxableServices: false, taxableShipping: false, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  MD: { stateCode: 'MD', stateName: 'Maryland', stateBaseRatePercent: 6.0, averageLocalRatePercent: 0.0, combinedRatePercent: 6.0, taxableServices: false, taxableShipping: false, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  MA: { stateCode: 'MA', stateName: 'Massachusetts', stateBaseRatePercent: 6.25, averageLocalRatePercent: 0.0, combinedRatePercent: 6.25, taxableServices: false, taxableShipping: false, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 0 },
  MI: { stateCode: 'MI', stateName: 'Michigan', stateBaseRatePercent: 6.0, averageLocalRatePercent: 0.0, combinedRatePercent: 6.0, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  MN: { stateCode: 'MN', stateName: 'Minnesota', stateBaseRatePercent: 6.875, averageLocalRatePercent: 0.61, combinedRatePercent: 7.49, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  MS: { stateCode: 'MS', stateName: 'Mississippi', stateBaseRatePercent: 7.0, averageLocalRatePercent: 0.07, combinedRatePercent: 7.07, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 25000000, economicNexusTransactionThreshold: 0 },
  MO: { stateCode: 'MO', stateName: 'Missouri', stateBaseRatePercent: 4.225, averageLocalRatePercent: 4.07, combinedRatePercent: 8.29, taxableServices: false, taxableShipping: false, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 0 },
  MT: { stateCode: 'MT', stateName: 'Montana', stateBaseRatePercent: 0.0, averageLocalRatePercent: 0.0, combinedRatePercent: 0.0, taxableServices: false, taxableShipping: false, economicNexusSalesThresholdCents: 0, economicNexusTransactionThreshold: 0 },
  NE: { stateCode: 'NE', stateName: 'Nebraska', stateBaseRatePercent: 5.5, averageLocalRatePercent: 1.44, combinedRatePercent: 6.94, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  NV: { stateCode: 'NV', stateName: 'Nevada', stateBaseRatePercent: 6.85, averageLocalRatePercent: 1.38, combinedRatePercent: 8.23, taxableServices: false, taxableShipping: false, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  NH: { stateCode: 'NH', stateName: 'New Hampshire', stateBaseRatePercent: 0.0, averageLocalRatePercent: 0.0, combinedRatePercent: 0.0, taxableServices: false, taxableShipping: false, economicNexusSalesThresholdCents: 0, economicNexusTransactionThreshold: 0 },
  NJ: { stateCode: 'NJ', stateName: 'New Jersey', stateBaseRatePercent: 6.625, averageLocalRatePercent: 0.0, combinedRatePercent: 6.625, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  NM: { stateCode: 'NM', stateName: 'New Mexico', stateBaseRatePercent: 5.0, averageLocalRatePercent: 2.72, combinedRatePercent: 7.72, taxableServices: true, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 0 },
  NY: { stateCode: 'NY', stateName: 'New York', stateBaseRatePercent: 4.0, averageLocalRatePercent: 4.52, combinedRatePercent: 8.52, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 50000000, economicNexusTransactionThreshold: 100 },
  NC: { stateCode: 'NC', stateName: 'North Carolina', stateBaseRatePercent: 4.75, averageLocalRatePercent: 2.25, combinedRatePercent: 7.0, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  ND: { stateCode: 'ND', stateName: 'North Dakota', stateBaseRatePercent: 5.0, averageLocalRatePercent: 1.96, combinedRatePercent: 6.96, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 0 },
  OH: { stateCode: 'OH', stateName: 'Ohio', stateBaseRatePercent: 5.75, averageLocalRatePercent: 1.49, combinedRatePercent: 7.24, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  OK: { stateCode: 'OK', stateName: 'Oklahoma', stateBaseRatePercent: 4.5, averageLocalRatePercent: 4.47, combinedRatePercent: 8.97, taxableServices: false, taxableShipping: false, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 0 },
  OR: { stateCode: 'OR', stateName: 'Oregon', stateBaseRatePercent: 0.0, averageLocalRatePercent: 0.0, combinedRatePercent: 0.0, taxableServices: false, taxableShipping: false, economicNexusSalesThresholdCents: 0, economicNexusTransactionThreshold: 0 },
  PA: { stateCode: 'PA', stateName: 'Pennsylvania', stateBaseRatePercent: 6.0, averageLocalRatePercent: 0.34, combinedRatePercent: 6.34, taxableServices: false, taxableShipping: false, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 0 },
  RI: { stateCode: 'RI', stateName: 'Rhode Island', stateBaseRatePercent: 7.0, averageLocalRatePercent: 0.0, combinedRatePercent: 7.0, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  SC: { stateCode: 'SC', stateName: 'South Carolina', stateBaseRatePercent: 6.0, averageLocalRatePercent: 1.44, combinedRatePercent: 7.44, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 0 },
  SD: { stateCode: 'SD', stateName: 'South Dakota', stateBaseRatePercent: 4.5, averageLocalRatePercent: 1.9, combinedRatePercent: 6.4, taxableServices: true, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  TN: { stateCode: 'TN', stateName: 'Tennessee', stateBaseRatePercent: 7.0, averageLocalRatePercent: 2.55, combinedRatePercent: 9.55, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 0 },
  TX: { stateCode: 'TX', stateName: 'Texas', stateBaseRatePercent: 6.25, averageLocalRatePercent: 1.95, combinedRatePercent: 8.2, taxableServices: true, taxableShipping: true, economicNexusSalesThresholdCents: 50000000, economicNexusTransactionThreshold: 0 },
  UT: { stateCode: 'UT', stateName: 'Utah', stateBaseRatePercent: 6.1, averageLocalRatePercent: 1.09, combinedRatePercent: 7.19, taxableServices: true, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  VT: { stateCode: 'VT', stateName: 'Vermont', stateBaseRatePercent: 6.0, averageLocalRatePercent: 0.24, combinedRatePercent: 6.24, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  VA: { stateCode: 'VA', stateName: 'Virginia', stateBaseRatePercent: 5.3, averageLocalRatePercent: 0.45, combinedRatePercent: 5.75, taxableServices: false, taxableShipping: false, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  WA: { stateCode: 'WA', stateName: 'Washington', stateBaseRatePercent: 6.5, averageLocalRatePercent: 2.79, combinedRatePercent: 9.29, taxableServices: true, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 0 },
  WV: { stateCode: 'WV', stateName: 'West Virginia', stateBaseRatePercent: 6.0, averageLocalRatePercent: 0.55, combinedRatePercent: 6.55, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  WI: { stateCode: 'WI', stateName: 'Wisconsin', stateBaseRatePercent: 5.0, averageLocalRatePercent: 0.43, combinedRatePercent: 5.43, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 0 },
  WY: { stateCode: 'WY', stateName: 'Wyoming', stateBaseRatePercent: 4.0, averageLocalRatePercent: 1.36, combinedRatePercent: 5.36, taxableServices: false, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
  DC: { stateCode: 'DC', stateName: 'District of Columbia', stateBaseRatePercent: 6.0, averageLocalRatePercent: 0.0, combinedRatePercent: 6.0, taxableServices: true, taxableShipping: true, economicNexusSalesThresholdCents: 10000000, economicNexusTransactionThreshold: 200 },
};

export class ComprehensiveTaxEngine {
  public static calculateSalesTax(stateCode: string, taxableAmountCents: number, shippingFeeCents: number = 0): { taxAmountCents: number; ratePercent: number; stateBaseCents: number; localJurisdictionCents: number } {
    const rule = US_STATE_TAX_MATRIX[stateCode.toUpperCase()];
    if (!rule) {
      return { taxAmountCents: 0, ratePercent: 0, stateBaseCents: 0, localJurisdictionCents: 0 };
    }

    const eligibleBase = taxableAmountCents + (rule.taxableShipping ? shippingFeeCents : 0);
    const stateBaseCents = Math.round((eligibleBase * rule.stateBaseRatePercent) / 100);
    const localJurisdictionCents = Math.round((eligibleBase * rule.averageLocalRatePercent) / 100);
    const totalTax = stateBaseCents + localJurisdictionCents;

    return {
      taxAmountCents: totalTax,
      ratePercent: rule.combinedRatePercent,
      stateBaseCents,
      localJurisdictionCents
    };
  }
}
