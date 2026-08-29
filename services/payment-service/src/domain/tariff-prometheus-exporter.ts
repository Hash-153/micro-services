export class TariffPrometheusExporter {
  public static exportMetrics(mappedCategories: number, unmappedCategories: number): string {
    return [
      '# HELP payment_commodity_code_mapped_categories Total number of catalog categories with mapped UNSPSC commodity codes',
      '# TYPE payment_commodity_code_mapped_categories gauge',
      `payment_commodity_code_mapped_categories ${mappedCategories}`,
      '# HELP payment_commodity_code_unmapped_categories Total number of catalog categories lacking UNSPSC mapping',
      '# TYPE payment_commodity_code_unmapped_categories gauge',
      `payment_commodity_code_unmapped_categories ${unmappedCategories}`
    ].join('\n');
  }
}
