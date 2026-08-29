import { CurrencyConverter } from '../../services/payment-service/src/domain/currency-exchange-rate.js';
import { Currency } from '@novacommerce/core-types';

describe('E2E Scenario: Multi-Currency Checkout & Real-Time FX Conversion', () => {
  it('should convert cart totals accurately into EUR and GBP with spread', () => {
    const usdMoney = { amount: 25000, currency: Currency.USD }; // $250.00
    const eurMoney = CurrencyConverter.convert(usdMoney, Currency.EUR, 0.5);
    const gbpMoney = CurrencyConverter.convert(usdMoney, Currency.GBP, 0.5);

    expect(eurMoney.currency).toBe(Currency.EUR);
    expect(eurMoney.amount).toBeGreaterThan(20000);
    expect(gbpMoney.currency).toBe(Currency.GBP);
    expect(gbpMoney.amount).toBeGreaterThan(18000);
  });
});
