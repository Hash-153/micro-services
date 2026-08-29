import { Level3ProcessingPayload } from './level3-card-data-builder.js';

export class Level3YamlFormatter {
  public static formatYaml(payload: Level3ProcessingPayload): string {
    const lines = [
      `summaryCommodityCode: "${payload.summaryCommodityCode}"`,
      `freightAmountCents: ${payload.freightAmountCents}`,
      `dutyAmountCents: ${payload.dutyAmountCents}`,
      `shipFromPostalCode: "${payload.shipFromPostalCode}"`,
      `destinationPostalCode: "${payload.destinationPostalCode}"`,
      `destinationCountryCode: "${payload.destinationCountryCode}"`,
      `lineItems:`
    ];

    for (const it of payload.lineItems) {
      lines.push(`  - commodityCode: "${it.itemCommodityCode}"`);
      lines.push(`    description: "${it.itemDescription}"`);
      lines.push(`    productCode: "${it.productCode}"`);
      lines.push(`    quantity: ${it.quantity}`);
      lines.push(`    unitCostCents: ${it.unitCostCents}`);
      lines.push(`    totalAmountCents: ${it.totalAmountCents}`);
    }

    return lines.join('\n');
  }
}
