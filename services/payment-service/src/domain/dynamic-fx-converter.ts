import { Currency } from '@novacommerce/core-types';

export interface FxRatePair {
  baseCurrency: Currency;
  targetCurrency: Currency;
  rate: number;
  spreadBasisPoints: number;
  lastUpdatedAt: Date;
}

export class DynamicFxConverter {
  private static readonly BASE_RATES: Map<string, FxRatePair> = new Map();

  static {
    const pairs: [Currency, Currency, number][] = [
      [Currency.USD, Currency.EUR, 0.92],
      [Currency.USD, Currency.GBP, 0.79],
      [Currency.USD, Currency.CAD, 1.36],
      [Currency.USD, Currency.AUD, 1.52],
      [Currency.USD, Currency.JPY, 155.40],
      [Currency.USD, Currency.CHF, 0.90],
      [Currency.USD, Currency.SGD, 1.35],
      [Currency.USD, Currency.INR, 83.45],
      [Currency.EUR, Currency.USD, 1.087],
      [Currency.GBP, Currency.USD, 1.265]
    ];

    for (const [base, target, rate] of pairs) {
      const key = `${base}:${target}`;
      this.BASE_RATES.set(key, {
        baseCurrency: base,
        targetCurrency: target,
        rate,
        spreadBasisPoints: 25, // 0.25% margin
        lastUpdatedAt: new Date()
      });
    }
  }

  public static convert(
    amountCents: number,
    fromCurrency: Currency,
    toCurrency: Currency
  ): { convertedAmountCents: number; effectiveRate: number; feeCents: number } {
    if (fromCurrency === toCurrency) {
      return { convertedAmountCents: amountCents, effectiveRate: 1.0, feeCents: 0 };
    }

    const key = `${fromCurrency}:${toCurrency}`;
    const pair = this.BASE_RATES.get(key);

    if (!pair) {
      throw new Error(`Unsupported currency conversion pair: ${fromCurrency} to ${toCurrency}`);
    }

    const spreadMultiplier = 1 + pair.spreadBasisPoints / 10000;
    const effectiveRate = pair.rate * spreadMultiplier;
    const converted = Math.round(amountCents * effectiveRate);
    const fee = Math.round(amountCents * (pair.spreadBasisPoints / 10000));

    return {
      convertedAmountCents: converted,
      effectiveRate: Math.round(effectiveRate * 10000) / 10000,
      feeCents: fee
    };
  }
}
