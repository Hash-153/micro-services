export interface ItemCustomAttribute {
  name: string;
  value: string;
}

export class LineItemCustomAttributeExtractor {
  public static extractAttributes(rawMetadata: Record<string, any>): ItemCustomAttribute[] {
    return Object.entries(rawMetadata).map(([name, value]) => ({
      name,
      value: String(value)
    }));
  }
}
