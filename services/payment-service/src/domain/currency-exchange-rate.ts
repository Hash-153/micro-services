import { Currency, Money } from '@novacommerce/core-types';

export interface ExchangeRateQuote {
  baseCurrency: Currency;
  targetCurrency: Currency;
  rate: number;
  spreadPercent: number;
  effectiveRate: number;
  expiresAt: Date;
}

export const BASE_FX_RATES_TO_USD: Record<Currency, number> = {
  [Currency.USD]: 1.0,
  [Currency.EUR]: 1.08,
  [Currency.GBP]: 1.28,
  [Currency.CAD]: 0.74,
  [Currency.AUD]: 0.66,
  [Currency.JPY]: 0.0065,
  [Currency.CHF]: 1.13,
  [Currency.SGD]: 0.75,
  [Currency.INR]: 0.012
};

export class CurrencyConverter {
  public static convert(money: Money, targetCurrency: Currency, spreadPercent: number = 0.5): Money {
    if (money.currency === targetCurrency) {
      return money;
    }

    const baseToUsd = BASE_FX_RATES_TO_USD[money.currency] || 1.0;
    const targetToUsd = BASE_FX_RATES_TO_USD[targetCurrency] || 1.0;

    // Convert source amount to USD, then USD to target
    const amountInUsd = money.amount * baseToUsd;
    const rawTargetAmount = amountInUsd / targetToUsd;
    
    // Apply spread
    const spreadMultiplier = 1 + (spreadPercent / 100);
    const convertedAmount = Math.round(rawTargetAmount * spreadMultiplier);

    return {
      amount: convertedAmount,
      currency: targetCurrency
    };
  }
}
