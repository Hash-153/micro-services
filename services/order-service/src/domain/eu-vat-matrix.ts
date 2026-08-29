export interface EuVatCountryRate {
  countryCode: string;
  countryName: string;
  standardRatePercent: number;
  reducedRatePercent: number;
  superReducedRatePercent?: number;
  digitalServicesRatePercent: number;
  isEuMember: boolean;
}

export const EU_VAT_COUNTRY_RATES: Record<string, EuVatCountryRate> = {
  AT: { countryCode: 'AT', countryName: 'Austria', standardRatePercent: 20.0, reducedRatePercent: 10.0, digitalServicesRatePercent: 20.0, isEuMember: true },
  BE: { countryCode: 'BE', countryName: 'Belgium', standardRatePercent: 21.0, reducedRatePercent: 12.0, digitalServicesRatePercent: 21.0, isEuMember: true },
  BG: { countryCode: 'BG', countryName: 'Bulgaria', standardRatePercent: 20.0, reducedRatePercent: 9.0, digitalServicesRatePercent: 20.0, isEuMember: true },
  HR: { countryCode: 'HR', countryName: 'Croatia', standardRatePercent: 25.0, reducedRatePercent: 13.0, digitalServicesRatePercent: 25.0, isEuMember: true },
  CY: { countryCode: 'CY', countryName: 'Cyprus', standardRatePercent: 19.0, reducedRatePercent: 9.0, digitalServicesRatePercent: 19.0, isEuMember: true },
  CZ: { countryCode: 'CZ', countryName: 'Czech Republic', standardRatePercent: 21.0, reducedRatePercent: 12.0, digitalServicesRatePercent: 21.0, isEuMember: true },
  DK: { countryCode: 'DK', countryName: 'Denmark', standardRatePercent: 25.0, reducedRatePercent: 0.0, digitalServicesRatePercent: 25.0, isEuMember: true },
  EE: { countryCode: 'EE', countryName: 'Estonia', standardRatePercent: 22.0, reducedRatePercent: 9.0, digitalServicesRatePercent: 22.0, isEuMember: true },
  FI: { countryCode: 'FI', countryName: 'Finland', standardRatePercent: 24.0, reducedRatePercent: 14.0, digitalServicesRatePercent: 24.0, isEuMember: true },
  FR: { countryCode: 'FR', countryName: 'France', standardRatePercent: 20.0, reducedRatePercent: 10.0, digitalServicesRatePercent: 20.0, isEuMember: true },
  DE: { countryCode: 'DE', countryName: 'Germany', standardRatePercent: 19.0, reducedRatePercent: 7.0, digitalServicesRatePercent: 19.0, isEuMember: true },
  GR: { countryCode: 'GR', countryName: 'Greece', standardRatePercent: 24.0, reducedRatePercent: 13.0, digitalServicesRatePercent: 24.0, isEuMember: true },
  HU: { countryCode: 'HU', countryName: 'Hungary', standardRatePercent: 27.0, reducedRatePercent: 18.0, digitalServicesRatePercent: 27.0, isEuMember: true },
  IE: { countryCode: 'IE', countryName: 'Ireland', standardRatePercent: 23.0, reducedRatePercent: 13.5, digitalServicesRatePercent: 23.0, isEuMember: true },
  IT: { countryCode: 'IT', countryName: 'Italy', standardRatePercent: 22.0, reducedRatePercent: 10.0, digitalServicesRatePercent: 22.0, isEuMember: true },
  LV: { countryCode: 'LV', countryName: 'Latvia', standardRatePercent: 21.0, reducedRatePercent: 12.0, digitalServicesRatePercent: 21.0, isEuMember: true },
  LT: { countryCode: 'LT', countryName: 'Lithuania', standardRatePercent: 21.0, reducedRatePercent: 9.0, digitalServicesRatePercent: 21.0, isEuMember: true },
  LU: { countryCode: 'LU', countryName: 'Luxembourg', standardRatePercent: 17.0, reducedRatePercent: 14.0, digitalServicesRatePercent: 17.0, isEuMember: true },
  MT: { countryCode: 'MT', countryName: 'Malta', standardRatePercent: 18.0, reducedRatePercent: 7.0, digitalServicesRatePercent: 18.0, isEuMember: true },
  NL: { countryCode: 'NL', countryName: 'Netherlands', standardRatePercent: 21.0, reducedRatePercent: 9.0, digitalServicesRatePercent: 21.0, isEuMember: true },
  PL: { countryCode: 'PL', countryName: 'Poland', standardRatePercent: 23.0, reducedRatePercent: 8.0, digitalServicesRatePercent: 23.0, isEuMember: true },
  PT: { countryCode: 'PT', countryName: 'Portugal', standardRatePercent: 23.0, reducedRatePercent: 13.0, digitalServicesRatePercent: 23.0, isEuMember: true },
  RO: { countryCode: 'RO', countryName: 'Romania', standardRatePercent: 19.0, reducedRatePercent: 9.0, digitalServicesRatePercent: 19.0, isEuMember: true },
  SK: { countryCode: 'SK', countryName: 'Slovakia', standardRatePercent: 20.0, reducedRatePercent: 10.0, digitalServicesRatePercent: 20.0, isEuMember: true },
  SI: { countryCode: 'SI', countryName: 'Slovenia', standardRatePercent: 22.0, reducedRatePercent: 9.5, digitalServicesRatePercent: 22.0, isEuMember: true },
  ES: { countryCode: 'ES', countryName: 'Spain', standardRatePercent: 21.0, reducedRatePercent: 10.0, digitalServicesRatePercent: 21.0, isEuMember: true },
  SE: { countryCode: 'SE', countryName: 'Sweden', standardRatePercent: 25.0, reducedRatePercent: 12.0, digitalServicesRatePercent: 25.0, isEuMember: true },
  GB: { countryCode: 'GB', countryName: 'United Kingdom (Post-Brexit)', standardRatePercent: 20.0, reducedRatePercent: 5.0, digitalServicesRatePercent: 20.0, isEuMember: true },
  CH: { countryCode: 'CH', countryName: 'Switzerland', standardRatePercent: 8.1, reducedRatePercent: 2.6, digitalServicesRatePercent: 8.1, isEuMember: true },
  NO: { countryCode: 'NO', countryName: 'Norway', standardRatePercent: 25.0, reducedRatePercent: 15.0, digitalServicesRatePercent: 25.0, isEuMember: true },
};

export class EuVatCalculator {
  public static calculateVat(countryCode: string, amountCents: number, isB2bWithValidVatId: boolean = false): { vatAmountCents: number; ratePercent: number; isReverseChargeApplied: boolean } {
    if (isB2bWithValidVatId) {
      return { vatAmountCents: 0, ratePercent: 0, isReverseChargeApplied: true };
    }

    const country = EU_VAT_COUNTRY_RATES[countryCode.toUpperCase()];
    if (!country) {
      return { vatAmountCents: 0, ratePercent: 0, isReverseChargeApplied: false };
    }

    const vat = Math.round((amountCents * country.standardRatePercent) / 100);
    return {
      vatAmountCents: vat,
      ratePercent: country.standardRatePercent,
      isReverseChargeApplied: false
    };
  }
}
