export interface TaxCalculationResult {
  stateCode: string;
  taxableAmountCents: number;
  taxRatePercent: number;
  taxAmountCents: number;
  jurisdiction: string;
  isExempt: boolean;
}

export class USTaxEngine {
  private static readonly STATE_RATES: Record<string, { rate: number; name: string }> = {
    AL: { rate: 4.00, name: 'Alabama' },
    AK: { rate: 0.00, name: 'Alaska' },
    AZ: { rate: 5.60, name: 'Arizona' },
    AR: { rate: 6.50, name: 'Arkansas' },
    CA: { rate: 7.25, name: 'California' },
    CO: { rate: 2.90, name: 'Colorado' },
    CT: { rate: 6.35, name: 'Connecticut' },
    DE: { rate: 0.00, name: 'Delaware' },
    FL: { rate: 6.00, name: 'Florida' },
    GA: { rate: 4.00, name: 'Georgia' },
    HI: { rate: 4.00, name: 'Hawaii' },
    ID: { rate: 6.00, name: 'Idaho' },
    IL: { rate: 6.25, name: 'Illinois' },
    IN: { rate: 7.00, name: 'Indiana' },
    IA: { rate: 6.00, name: 'Iowa' },
    KS: { rate: 6.50, name: 'Kansas' },
    KY: { rate: 6.00, name: 'Kentucky' },
    LA: { rate: 4.45, name: 'Louisiana' },
    ME: { rate: 5.50, name: 'Maine' },
    MD: { rate: 6.00, name: 'Maryland' },
    MA: { rate: 6.25, name: 'Massachusetts' },
    MI: { rate: 6.00, name: 'Michigan' },
    MN: { rate: 6.875, name: 'Minnesota' },
    MS: { rate: 7.00, name: 'Mississippi' },
    MO: { rate: 4.225, name: 'Missouri' },
    MT: { rate: 0.00, name: 'Montana' },
    NE: { rate: 5.50, name: 'Nebraska' },
    NV: { rate: 6.85, name: 'Nevada' },
    NH: { rate: 0.00, name: 'New Hampshire' },
    NJ: { rate: 6.625, name: 'New Jersey' },
    NM: { rate: 5.00, name: 'New Mexico' },
    NY: { rate: 4.00, name: 'New York' },
    NC: { rate: 4.75, name: 'North Carolina' },
    ND: { rate: 5.00, name: 'North Dakota' },
    OH: { rate: 5.75, name: 'Ohio' },
    OK: { rate: 4.50, name: 'Oklahoma' },
    OR: { rate: 0.00, name: 'Oregon' },
    PA: { rate: 6.00, name: 'Pennsylvania' },
    RI: { rate: 7.00, name: 'Rhode Island' },
    SC: { rate: 6.00, name: 'South Carolina' },
    SD: { rate: 4.20, name: 'South Dakota' },
    TN: { rate: 7.00, name: 'Tennessee' },
    TX: { rate: 6.25, name: 'Texas' },
    UT: { rate: 6.10, name: 'Utah' },
    VT: { rate: 6.00, name: 'Vermont' },
    VA: { rate: 5.30, name: 'Virginia' },
    WA: { rate: 6.50, name: 'Washington' },
    WV: { rate: 6.00, name: 'West Virginia' },
    WI: { rate: 5.00, name: 'Wisconsin' },
    WY: { rate: 4.00, name: 'Wyoming' },
    DC: { rate: 6.00, name: 'District of Columbia' }
  };

  public static calculate(amountCents: number, stateCode: string): TaxCalculationResult {
    const normalized = stateCode.toUpperCase().trim();
    const config = this.STATE_RATES[normalized];

    if (!config) {
      // Default to zero tax for unrecognized international jurisdiction
      return {
        stateCode: normalized,
        taxableAmountCents: amountCents,
        taxRatePercent: 0.0,
        taxAmountCents: 0,
        jurisdiction: 'Default Jurisdiction',
        isExempt: true
      };
    }

    const taxAmountCents = Math.round((amountCents * config.rate) / 100);
    return {
      stateCode: normalized,
      taxableAmountCents: amountCents,
      taxRatePercent: config.rate,
      taxAmountCents,
      jurisdiction: config.name,
      isExempt: config.rate === 0.0
    };
  }
}
