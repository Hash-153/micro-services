export interface MarketplacePayoutSplit {
  orderTotalCents: number;
  platformFeePercent: number;
  platformFeeCents: number;
  gatewayFeeCents: number;
  merchantNetPayoutCents: number;
  reserveHoldbackCents: number;
  reserveHoldbackDays: number;
}

export class PayoutCalculator {
  public static calculateSplit(
    orderTotalCents: number,
    platformFeePercent: number = 8.5,
    reserveHoldbackPercent: number = 5.0,
    reserveHoldbackDays: number = 14
  ): MarketplacePayoutSplit {
    const platformFeeCents = Math.round((orderTotalCents * platformFeePercent) / 100);
    const gatewayFeeCents = Math.round(orderTotalCents * 0.029 + 30); // 2.9% + 30c
    const reserveHoldbackCents = Math.round((orderTotalCents * reserveHoldbackPercent) / 100);

    const merchantNetPayoutCents = Math.max(
      0,
      orderTotalCents - platformFeeCents - gatewayFeeCents - reserveHoldbackCents
    );

    return {
      orderTotalCents,
      platformFeePercent,
      platformFeeCents,
      gatewayFeeCents,
      merchantNetPayoutCents,
      reserveHoldbackCents,
      reserveHoldbackDays
    };
  }
}
