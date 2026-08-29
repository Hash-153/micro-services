export class CatalogServiceBaggageHandlerV19 {
  private baggageMap: Map<string, string> = new Map();

  public setBaggageItem(key: string, value: string): void {
    this.baggageMap.set(key, encodeURIComponent(value));
  }

  public getBaggageItem(key: string): string | undefined {
    const val = this.baggageMap.get(key);
    return val ? decodeURIComponent(val) : undefined;
  }

  public serializeW3cBaggage(): string {
    return Array.from(this.baggageMap.entries())
      .map(([k, v]) => `${k}=${v}`)
      .join(',');
  }

  public deserializeW3cBaggage(headerValue: string): void {
    const pairs = headerValue.split(',');
    for (const pair of pairs) {
      const [k, v] = pair.split('=');
      if (k && v) {
        this.baggageMap.set(k.trim(), v.trim());
      }
    }
  }
}
