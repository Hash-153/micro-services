export class CommodityCodeNormalizer {
  public static normalizeCode(rawCode: string): string {
    const digits = rawCode.replace(/[^0-9]/g, '');
    if (digits.length === 8) {
      return `${digits.slice(0, 4)}.${digits.slice(4, 6)}.${digits.slice(6, 8)}`;
    }
    return rawCode.trim();
  }
}
