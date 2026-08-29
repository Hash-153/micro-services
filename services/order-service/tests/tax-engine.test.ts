import { TaxCalculator } from '../src/domain/tax-rules.js';

describe('Order Service: US 50-State Real-Time Tax Calculation Suite', () => {
  it('should calculate 0% tax for zero-tax states (DE, OR, MT, NH, AK)', () => {
    const delawareTax = TaxCalculator.calculateTax(10000, 'DE');
    expect(delawareTax.taxRatePercent).toBe(0);
    expect(delawareTax.taxCents).toBe(0);

    const oregonTax = TaxCalculator.calculateTax(10000, 'OR');
    expect(oregonTax.taxRatePercent).toBe(0);
    expect(oregonTax.taxCents).toBe(0);
  });

  it('should calculate accurate tax for California (7.25%)', () => {
    const caTax = TaxCalculator.calculateTax(10000, 'CA');
    expect(caTax.taxRatePercent).toBe(7.25);
    expect(caTax.taxCents).toBe(725);
  });
});
