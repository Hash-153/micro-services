import { Money, Currency } from '@novacommerce/core-types';

export interface SettlementBatchItem {
  transactionId: string;
  orderNumber: string;
  grossAmountCents: number;
  interchangeFeeCents: number;
  gatewayFeeCents: number;
  netPayoutCents: number;
  settledDate: string;
}

export class MerchantReconciliationReport {
  public static generateSummary(items: SettlementBatchItem[], currency: Currency = Currency.USD): {
    totalGrossAmountCents: number;
    totalInterchangeCents: number;
    totalGatewayFeeCents: number;
    totalNetPayoutCents: number;
    transactionCount: number;
    effectiveProcessingRatePercent: number;
  } {
    const totalGross = items.reduce((acc, it) => acc + it.grossAmountCents, 0);
    const totalInterchange = items.reduce((acc, it) => acc + it.interchangeFeeCents, 0);
    const totalGatewayFee = items.reduce((acc, it) => acc + it.gatewayFeeCents, 0);
    const totalNetPayout = items.reduce((acc, it) => acc + it.netPayoutCents, 0);
    const totalFees = totalInterchange + totalGatewayFee;

    const rate = totalGross > 0 ? (totalFees / totalGross) * 100 : 0;

    return {
      totalGrossAmountCents: totalGross,
      totalInterchangeCents: totalInterchange,
      totalGatewayFeeCents: totalGatewayFee,
      totalNetPayoutCents: totalNetPayout,
      transactionCount: items.length,
      effectiveProcessingRatePercent: Math.round(rate * 100) / 100
    };
  }
}
