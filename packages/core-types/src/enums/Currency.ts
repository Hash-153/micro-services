export enum Currency {
  USD = 'USD',
  EUR = 'EUR',
  GBP = 'GBP',
  CAD = 'CAD',
  AUD = 'AUD',
  JPY = 'JPY',
  CHF = 'CHF',
  SGD = 'SGD',
  INR = 'INR'
}

export interface Money {
  amount: number; // Stored in minor currency units (cents, pence, etc.)
  currency: Currency;
}
