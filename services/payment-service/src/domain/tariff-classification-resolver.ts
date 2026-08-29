import { CommodityCodeMapping, COMMODITY_CODE_REGISTRY } from './commodity-code-classifier.js';

export class TariffClassificationResolver {
  public static resolveByKeyword(keyword: string): CommodityCodeMapping[] {
    const lower = keyword.toLowerCase();
    return COMMODITY_CODE_REGISTRY.filter(
      c => c.categorySlug.includes(lower) || c.description.toLowerCase().includes(lower)
    );
  }
}
