export interface UserActivitySummary {
  userId: string;
  daysSinceLastLogin: number;
  ordersLast30Days: number;
  ordersPrevious30To60Days: number;
  supportTicketsLast30Days: number;
  unsubscribedMarketing: boolean;
}

export class ChurnPredictor {
  public static evaluateChurnRisk(activity: UserActivitySummary): { churnRiskScore: number; riskLevel: 'LOW' | 'MEDIUM' | 'HIGH'; churnFactors: string[] } {
    let score = 0;
    const factors: string[] = [];

    if (activity.daysSinceLastLogin >= 30) {
      score += 40;
      factors.push('Inactive for over 30 days');
    } else if (activity.daysSinceLastLogin >= 14) {
      score += 20;
      factors.push('Inactive for over 14 days');
    }

    if (activity.ordersPrevious30To60Days > 0 && activity.ordersLast30Days === 0) {
      score += 30;
      factors.push('Purchasing activity dropped to zero in past 30 days');
    }

    if (activity.supportTicketsLast30Days >= 3) {
      score += 20;
      factors.push('Elevated support friction in past 30 days');
    }

    if (activity.unsubscribedMarketing) {
      score += 10;
      factors.push('Unsubscribed from marketing communications');
    }

    let riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' = 'LOW';
    if (score >= 60) riskLevel = 'HIGH';
    else if (score >= 30) riskLevel = 'MEDIUM';

    return {
      churnRiskScore: score,
      riskLevel,
      churnFactors: factors
    };
  }
}
