export class CavvCryptogramValidator {
  public static validateCavv(cavvBase64: string, eciFlag: string): { isValid: boolean; reason?: string } {
    if (!cavvBase64 || cavvBase64.length < 28) {
      return { isValid: false, reason: 'CAVV cryptogram must be at least 28 characters Base64 string.' };
    }

    const validEciFlags = ['01', '02', '05', '06']; // Visa / Mastercard 3DS authenticated / liability shift
    if (!validEciFlags.includes(eciFlag)) {
      return { isValid: false, reason: `ECI flag '${eciFlag}' does not grant liability shift.` };
    }

    return { isValid: true };
  }
}
