export interface CustomerRfmInput {
  userId: string;
  daysSinceLastOrder: number;
  totalOrdersLifetime: number;
  totalSpendLifetimeCents: number;
}

export interface RfmSegmentResult {
  userId: string;
  recencyScore: number; // 1-5
  frequencyScore: number; // 1-5
  monetaryScore: number; // 1-5
  rfmSegment: 'CHAMPION' | 'LOYAL_CUSTOMER' | 'POTENTIAL_LOYALIST' | 'AT_RISK' | 'HIBERNATING' | 'LOST';
}

export class RfmScoringEngine {
  public static calculateRfm(input: CustomerRfmInput): RfmSegmentResult {
    // Recency scoring (1 = stale > 180 days, 5 = recent < 14 days)
    let r = 1;
    if (input.daysSinceLastOrder <= 14) r = 5;
    else if (input.daysSinceLastOrder <= 30) r = 4;
    else if (input.daysSinceLastOrder <= 60) r = 3;
    else if (input.daysSinceLastOrder <= 180) r = 2;

    // Frequency scoring (1 = 1 order, 5 = > 10 orders)
    let f = 1;
    if (input.totalOrdersLifetime >= 10) f = 5;
    else if (input.totalOrdersLifetime >= 6) f = 4;
    else if (input.totalOrdersLifetime >= 3) f = 3;
    else if (input.totalOrdersLifetime >= 2) f = 2;

    // Monetary scoring (1 = < $100, 5 = > $5,000)
    let m = 1;
    if (input.totalSpendLifetimeCents >= 500000) m = 5;
    else if (input.totalSpendLifetimeCents >= 200000) m = 4;
    else if (input.totalSpendLifetimeCents >= 100000) m = 3;
    else if (input.totalSpendLifetimeCents >= 30000) m = 2;

    let segment: RfmSegmentResult['rfmSegment'] = 'HIBERNATING';
    if (r >= 4 && f >= 4 && m >= 4) segment = 'CHAMPION';
    else if (f >= 3 && m >= 3) segment = 'LOYAL_CUSTOMER';
    else if (r >= 4 && f <= 2) segment = 'POTENTIAL_LOYALIST';
    else if (r <= 2 && f >= 3) segment = 'AT_RISK';
    else if (r === 1 && f === 1) segment = 'LOST';

    return {
      userId: input.userId,
      recencyScore: r,
      frequencyScore: f,
      monetaryScore: m,
      rfmSegment: segment
    };
  }
}
