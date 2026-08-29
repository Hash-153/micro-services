import { Currency } from '@novacommerce/core-types';

export interface CurrencyFormattingSpec {
  currency: Currency;
  minorUnitDecimalPlaces: number;
  symbol: string;
  symbolPlacement: 'BEFORE' | 'AFTER';
  thousandsSeparator: string;
  decimalSeparator: string;
}

export const CURRENCY_FORMATTING_SPECS: Record<Currency, CurrencyFormattingSpec> = {
  [Currency.USD]: { currency: Currency.USD, minorUnitDecimalPlaces: 2, symbol: '$', symbolPlacement: 'BEFORE', thousandsSeparator: ',', decimalSeparator: '.' },
  [Currency.EUR]: { currency: Currency.EUR, minorUnitDecimalPlaces: 2, symbol: '€', symbolPlacement: 'AFTER', thousandsSeparator: '.', decimalSeparator: ',' },
  [Currency.GBP]: { currency: Currency.GBP, minorUnitDecimalPlaces: 2, symbol: '£', symbolPlacement: 'BEFORE', thousandsSeparator: ',', decimalSeparator: '.' },
  [Currency.CAD]: { currency: Currency.CAD, minorUnitDecimalPlaces: 2, symbol: 'CA$', symbolPlacement: 'BEFORE', thousandsSeparator: ',', decimalSeparator: '.' },
  [Currency.AUD]: { currency: Currency.AUD, minorUnitDecimalPlaces: 2, symbol: 'AU$', symbolPlacement: 'BEFORE', thousandsSeparator: ',', decimalSeparator: '.' },
  [Currency.JPY]: { currency: Currency.JPY, minorUnitDecimalPlaces: 0, symbol: '¥', symbolPlacement: 'BEFORE', thousandsSeparator: ',', decimalSeparator: '.' },
  [Currency.CHF]: { currency: Currency.CHF, minorUnitDecimalPlaces: 2, symbol: 'CHF ', symbolPlacement: 'BEFORE', thousandsSeparator: "'", decimalSeparator: '.' },
  [Currency.SGD]: { currency: Currency.SGD, minorUnitDecimalPlaces: 2, symbol: 'SG$', symbolPlacement: 'BEFORE', thousandsSeparator: ',', decimalSeparator: '.' },
  [Currency.INR]: { currency: Currency.INR, minorUnitDecimalPlaces: 2, symbol: '₹', symbolPlacement: 'BEFORE', thousandsSeparator: ',', decimalSeparator: '.' }
};

export class CurrencyFormatter {
  public static format(amountCents: number, currency: Currency): string {
    const spec = CURRENCY_FORMATTING_SPECS[currency] || CURRENCY_FORMATTING_SPECS[Currency.USD];

    let formattedValue: string;
    if (spec.minorUnitDecimalPlaces === 0) {
      formattedValue = Math.round(amountCents / 100).toLocaleString('en-US');
    } else {
      const mainUnits = (amountCents / 100).toFixed(spec.minorUnitDecimalPlaces);
      const [whole, dec] = mainUnits.split('.');
      const wholeFormatted = whole.replace(/\B(?=(\d{3})+(?!\d))/g, spec.thousandsSeparator);
      formattedValue = `${wholeFormatted}${spec.decimalSeparator}${dec}`;
    }

    return spec.symbolPlacement === 'BEFORE'
      ? `${spec.symbol}${formattedValue}`
      : `${formattedValue} ${spec.symbol}`;
  }
}
