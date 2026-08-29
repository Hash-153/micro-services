import { Level3LineItemData } from './level3-card-data-builder.js';

export class LineItemTaxVerifier {
  public static verifyItemTax(item: Level3LineItemData, expectedTaxRatePercent: number): { isAccurate: boolean; expectedTaxCents: number; deltaCents: number } {
    const netAmount = item.totalAmountCents - item.discountAmountCents;
    const expectedTax = Math.round((netAmount * expectedTaxRatePercent) / 100);
    const delta = item.taxAmountCents - expectedTax;

    return {
      isAccurate: Math.abs(delta) <= 1, // Allow 1-cent rounding difference
      expectedTaxCents: expectedTax,
      deltaCents: delta
    };
  }
}
