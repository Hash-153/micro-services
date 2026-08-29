export class LineItemSanitizer {
  public static sanitizeDescription(rawDesc: string, maxLength: number = 26): string {
    const clean = rawDesc.replace(/[^a-zA-Z0-9\s-_.]/g, '').trim();
    if (clean.length <= maxLength) return clean;
    return clean.slice(0, maxLength);
  }

  public static sanitizeProductCode(sku: string, maxLength: number = 12): string {
    const clean = sku.replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
    return clean.slice(0, maxLength);
  }
}
