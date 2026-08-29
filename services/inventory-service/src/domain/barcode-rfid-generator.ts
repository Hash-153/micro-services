export class BarcodeRfidGenerator {
  public static generateEan13(skuCode: string, countryPrefix: string = '084'): string {
    const rawDigits = (countryPrefix + skuCode.replace(/[^0-9]/g, '').padEnd(9, '0')).slice(0, 12);

    let sum = 0;
    for (let i = 0; i < 12; i++) {
      const digit = parseInt(rawDigits.charAt(i), 10);
      sum += i % 2 === 0 ? digit : digit * 3;
    }

    const checkDigit = (10 - (sum % 10)) % 10;
    return `${rawDigits}${checkDigit}`;
  }

  public static generateEpcRfidTag(sku: string, serialNumber: number): string {
    const headerHex = '30'; // SGTIN-96
    const filter = '3';     // Item level
    const partition = '5';
    const skuHash = Buffer.from(sku).toString('hex').slice(0, 14).padEnd(14, '0');
    const serialHex = serialNumber.toString(16).padStart(8, '0');

    return `urn:epc:tag:sgtin-96:${filter}.${skuHash}.${serialHex}`;
  }
}
