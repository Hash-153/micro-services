import { CommodityCodeMapping, COMMODITY_CODE_REGISTRY } from './commodity-code-classifier.js';

export class TariffClassificationSeeder {
  public static generateSeedInserts(): string[] {
    return COMMODITY_CODE_REGISTRY.map(
      c => `INSERT INTO payment_commodity_codes (category_slug, unspsc_code, description, created_at) VALUES ('${c.categorySlug}', '${c.unspscCode}', '${c.description.replace(/'/g, "''")}', NOW()) ON CONFLICT (category_slug) DO NOTHING;`
    );
  }
}
