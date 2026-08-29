export class TaxIdentifierFormatter {
  public static normalizeEin(rawEin: string): string {
    const digits = rawEin.replace(/[^0-9]/g, '');
    if (digits.length !== 9) return rawEin;
    return `${digits.slice(0, 2)}-${digits.slice(2)}`;
  }

  public static normalizeVat(rawVat: string): string {
    return rawVat.replace(/[^A-Za-z0-9]/g, '').toUpperCase();
  }
}
