export interface CanadaProvinceTaxRate {
  provinceCode: string;
  provinceName: string;
  taxType: 'HST' | 'GST_PST' | 'GST_QST' | 'GST_ONLY';
  gstRatePercent: number;
  pstRatePercent: number;
  hstRatePercent: number;
  totalRatePercent: number;
}

export const CANADA_PROVINCIAL_TAX_MATRIX: Record<string, CanadaProvinceTaxRate> = {
  ON: { provinceCode: 'ON', provinceName: 'Ontario', taxType: 'HST', gstRatePercent: 0, pstRatePercent: 0, hstRatePercent: 13.0, totalRatePercent: 13.0 },
  BC: { provinceCode: 'BC', provinceName: 'British Columbia', taxType: 'GST_PST', gstRatePercent: 5.0, pstRatePercent: 7.0, hstRatePercent: 0, totalRatePercent: 12.0 },
  QC: { provinceCode: 'QC', provinceName: 'Quebec', taxType: 'GST_QST', gstRatePercent: 5.0, pstRatePercent: 9.975, hstRatePercent: 0, totalRatePercent: 14.975 },
  AB: { provinceCode: 'AB', provinceName: 'Alberta', taxType: 'GST_ONLY', gstRatePercent: 5.0, pstRatePercent: 0, hstRatePercent: 0, totalRatePercent: 5.0 },
  NS: { provinceCode: 'NS', provinceName: 'Nova Scotia', taxType: 'HST', gstRatePercent: 0, pstRatePercent: 0, hstRatePercent: 15.0, totalRatePercent: 15.0 },
  NB: { provinceCode: 'NB', provinceName: 'New Brunswick', taxType: 'HST', gstRatePercent: 0, pstRatePercent: 0, hstRatePercent: 15.0, totalRatePercent: 15.0 },
  MB: { provinceCode: 'MB', provinceName: 'Manitoba', taxType: 'GST_PST', gstRatePercent: 5.0, pstRatePercent: 7.0, hstRatePercent: 0, totalRatePercent: 12.0 },
  PE: { provinceCode: 'PE', provinceName: 'Prince Edward Island', taxType: 'HST', gstRatePercent: 0, pstRatePercent: 0, hstRatePercent: 15.0, totalRatePercent: 15.0 },
  SK: { provinceCode: 'SK', provinceName: 'Saskatchewan', taxType: 'GST_PST', gstRatePercent: 5.0, pstRatePercent: 6.0, hstRatePercent: 0, totalRatePercent: 11.0 },
  NL: { provinceCode: 'NL', provinceName: 'Newfoundland and Labrador', taxType: 'HST', gstRatePercent: 0, pstRatePercent: 0, hstRatePercent: 15.0, totalRatePercent: 15.0 },
  YT: { provinceCode: 'YT', provinceName: 'Yukon', taxType: 'GST_ONLY', gstRatePercent: 5.0, pstRatePercent: 0, hstRatePercent: 0, totalRatePercent: 5.0 },
  NT: { provinceCode: 'NT', provinceName: 'Northwest Territories', taxType: 'GST_ONLY', gstRatePercent: 5.0, pstRatePercent: 0, hstRatePercent: 0, totalRatePercent: 5.0 },
  NU: { provinceCode: 'NU', provinceName: 'Nunavut', taxType: 'GST_ONLY', gstRatePercent: 5.0, pstRatePercent: 0, hstRatePercent: 0, totalRatePercent: 5.0 }
};

export class CanadaTaxCalculator {
  public static calculateTax(provinceCode: string, taxableAmountCents: number): { gstAmountCents: number; pstAmountCents: number; hstAmountCents: number; totalTaxCents: number } {
    const rate = CANADA_PROVINCIAL_TAX_MATRIX[provinceCode.toUpperCase()] || CANADA_PROVINCIAL_TAX_MATRIX.ON;

    const gst = Math.round((taxableAmountCents * rate.gstRatePercent) / 100);
    const pst = Math.round((taxableAmountCents * rate.pstRatePercent) / 100);
    const hst = Math.round((taxableAmountCents * rate.hstRatePercent) / 100);

    return {
      gstAmountCents: gst,
      pstAmountCents: pst,
      hstAmountCents: hst,
      totalTaxCents: gst + pst + hst
    };
  }
}
