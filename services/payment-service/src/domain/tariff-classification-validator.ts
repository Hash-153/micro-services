export class TariffClassificationValidator {
  public static isValidUnspsc(code: string): boolean {
    // UNSPSC codes are exactly 8 digits
    return /^[0-9]{8}$/.test(code.replace(/\./g, ''));
  }

  public static isValidHsCode(code: string): boolean {
    // HS codes have 6 to 10 digits
    const clean = code.replace(/[^0-9]/g, '');
    return clean.length >= 6 && clean.length <= 10;
  }
}
