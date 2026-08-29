import { CurrencyConverter } from '../src/domain/currency-exchange-rate.js';
import { Currency } from '@novacommerce/core-types';

describe('Multi-Currency FX Exchange Engine Suite', () => {
  it('should return identical money object for same currency conversion', () => {
    const money = { amount: 5000, currency: Currency.USD };
    const res = CurrencyConverter.convert(money, Currency.USD);
    expect(res.amount).toBe(5000);
    expect(res.currency).toBe(Currency.USD);
  });

  it('should convert USD to EUR with spread correctly', () => {
    const money = { amount: 10000, currency: Currency.USD }; // $100.00
    const res = CurrencyConverter.convert(money, Currency.EUR, 0.5);
    expect(res.currency).toBe(Currency.EUR);
    expect(res.amount).toBeGreaterThan(9000);
    expect(res.amount).toBeLessThan(10000);
  });
});
