export interface InterchangeRateFee {
  cardScheme: 'VISA' | 'MASTERCARD' | 'AMEX' | 'DISCOVER';
  cardCategory: 'CONSUMER_CREDIT' | 'CONSUMER_DEBIT' | 'COMMERCIAL_CORPORATE' | 'INTERNATIONAL';
  interchangeRatePercent: number;
  perTransactionFeeCents: number;
  schemeAssessmentBps: number;
}

export const INTERCHANGE_RATE_TABLE: InterchangeRateFee[] = [
  { cardScheme: 'VISA', cardCategory: 'CONSUMER_DEBIT', interchangeRatePercent: 0.05, perTransactionFeeCents: 21, schemeAssessmentBps: 13 }, // Durbin regulated debit
  { cardScheme: 'VISA', cardCategory: 'CONSUMER_CREDIT', interchangeRatePercent: 1.51, perTransactionFeeCents: 10, schemeAssessmentBps: 14 },
  { cardScheme: 'VISA', cardCategory: 'COMMERCIAL_CORPORATE', interchangeRatePercent: 2.20, perTransactionFeeCents: 10, schemeAssessmentBps: 14 },
  { cardScheme: 'VISA', cardCategory: 'INTERNATIONAL', interchangeRatePercent: 1.95, perTransactionFeeCents: 10, schemeAssessmentBps: 55 },
  { cardScheme: 'MASTERCARD', cardCategory: 'CONSUMER_DEBIT', interchangeRatePercent: 0.05, perTransactionFeeCents: 21, schemeAssessmentBps: 13 },
  { cardScheme: 'MASTERCARD', cardCategory: 'CONSUMER_CREDIT', interchangeRatePercent: 1.58, perTransactionFeeCents: 10, schemeAssessmentBps: 14 },
  { cardScheme: 'MASTERCARD', cardCategory: 'COMMERCIAL_CORPORATE', interchangeRatePercent: 2.25, perTransactionFeeCents: 10, schemeAssessmentBps: 14 },
  { cardScheme: 'AMEX', cardCategory: 'CONSUMER_CREDIT', interchangeRatePercent: 2.30, perTransactionFeeCents: 10, schemeAssessmentBps: 16 }
];

export class InterchangePlusCalculator {
  public static calculateProcessingCosts(
    amountCents: number,
    cardScheme: 'VISA' | 'MASTERCARD' | 'AMEX' | 'DISCOVER',
    cardCategory: InterchangeRateFee['cardCategory'],
    acquirerMarkupBps: number = 20, // 0.20% processor markup
    acquirerPerTxnFeeCents: number = 10
  ): { totalFeeCents: number; interchangeCents: number; assessmentCents: number; acquirerMarkupCents: number } {
    const rate = INTERCHANGE_RATE_TABLE.find(r => r.cardScheme === cardScheme && r.cardCategory === cardCategory) || INTERCHANGE_RATE_TABLE[1];

    const interchangeCents = Math.round((amountCents * rate.interchangeRatePercent) / 100) + rate.perTransactionFeeCents;
    const assessmentCents = Math.round((amountCents * rate.schemeAssessmentBps) / 10000);
    const acquirerMarkupCents = Math.round((amountCents * acquirerMarkupBps) / 10000) + acquirerPerTxnFeeCents;

    const totalFee = interchangeCents + assessmentCents + acquirerMarkupCents;

    return {
      totalFeeCents: totalFee,
      interchangeCents,
      assessmentCents,
      acquirerMarkupCents
    };
  }
}
