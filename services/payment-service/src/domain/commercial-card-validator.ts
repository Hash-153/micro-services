export class CommercialCardValidator {
  public static isCommercialBin(bin: string): boolean {
    // Commercial card BIN range indicators
    const commercialBinPrefixes = ['4485', '4715', '5100', '5200', '5520', '3782', '3787'];
    return commercialBinPrefixes.some(prefix => bin.startsWith(prefix));
  }

  public static requiresTaxExemptCertificate(taxExemptNumber?: string): boolean {
    return Boolean(taxExemptNumber && taxExemptNumber.trim().length >= 8);
  }
}
