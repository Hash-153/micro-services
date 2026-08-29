import { CommodityCodeMapping } from './commodity-code-classifier.js';

export class TariffBulkImporter {
  public static parseCsv(csvContent: string): CommodityCodeMapping[] {
    const lines = csvContent.split('\n').filter(l => l.trim().length > 0);
    const mappings: CommodityCodeMapping[] = [];

    for (let i = 1; i < lines.length; i++) {
      const parts = lines[i].split(',');
      if (parts.length >= 3) {
        mappings.push({
          categorySlug: parts[0].trim(),
          unspscCode: parts[1].trim(),
          description: parts[2].trim().replace(/^"|"$/g, '')
        });
      }
    }

    return mappings;
  }
}
