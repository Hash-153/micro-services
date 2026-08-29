import { Money, Currency } from '@novacommerce/core-types';

export class TaxCalculator {
  // Calculates standard tax based on region and subtotal (e.g. 8.25%)
  public static calculateTax(subtotal: Money, countryCode: string = 'US', stateCode?: string): Money {
    let rate = 0.08; // Default 8%
    if (countryCode === 'DE' || countryCode === 'FR') rate = 0.19; // 19% VAT
    if (countryCode === 'GB') rate = 0.20; // 20% VAT
    if (stateCode === 'CA') rate = 0.0925;
    if (stateCode === 'NY') rate = 0.08875;

    const taxAmount = Math.round(subtotal.amount * rate);
    return {
      amount: taxAmount,
      currency: subtotal.currency
    };
  }
}
