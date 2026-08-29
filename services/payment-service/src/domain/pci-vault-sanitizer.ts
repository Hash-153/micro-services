export class PciVaultSanitizer {
  private static readonly PAN_REGEX = /\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b/g;
  private static readonly CVV_REGEX = /\b[0-9]{3,4}\b/g;

  public static maskPan(pan: string): string {
    const clean = pan.replace(/\s/g, '');
    if (clean.length < 10) return '***';
    const first6 = clean.slice(0, 6);
    const last4 = clean.slice(-4);
    const masked = '*'.repeat(clean.length - 10);
    return `${first6}${masked}${last4}`;
  }

  public static sanitizePayload<T>(payload: T): T {
    const jsonStr = JSON.stringify(payload);
    const sanitized = jsonStr.replace(this.PAN_REGEX, match => this.maskPan(match));
    return JSON.parse(sanitized);
  }
}
