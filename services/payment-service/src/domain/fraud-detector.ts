export interface FraudEvaluationContext {
  userId: string;
  orderId: string;
  amountCents: number;
  currency: string;
  ipAddress: string;
  cardBin: string;
  cardCountry: string;
  billingCountry: string;
  shippingCountry: string;
  deviceFingerprint: string;
  accountAgeDays: number;
  previousOrderCount: number;
  previousDisputeCount: number;
}

export interface FraudRiskScore {
  score: number; // 0 to 100
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  action: 'ALLOW' | 'CHALLENGE_3DS' | 'MANUAL_REVIEW' | 'REJECT';
  flaggedRules: string[];
}

export class FraudDetector {
  public static evaluateRisk(ctx: FraudEvaluationContext): FraudRiskScore {
    let score = 0;
    const flaggedRules: string[] = [];

    // Rule 1: High Transaction Velocity / Extreme Amount
    if (ctx.amountCents > 500000) { // > $5,000
      score += 25;
      flaggedRules.push('RULE_HIGH_TICKET_VALUE');
    }

    // Rule 2: Country Mismatch (Card Country vs Shipping Country)
    if (ctx.cardCountry && ctx.shippingCountry && ctx.cardCountry !== ctx.shippingCountry) {
      score += 30;
      flaggedRules.push('RULE_GEO_COUNTRY_MISMATCH');
    }

    // Rule 3: Brand new account with large purchase
    if (ctx.accountAgeDays < 1 && ctx.amountCents > 100000) {
      score += 20;
      flaggedRules.push('RULE_NEW_ACCOUNT_LARGE_AMOUNT');
    }

    // Rule 4: Historical Chargebacks / Disputes
    if (ctx.previousDisputeCount > 0) {
      score += 40;
      flaggedRules.push('RULE_PRIOR_DISPUTE_HISTORY');
    }

    // Rule 5: Disposable / Proxy IP Range (Simulated)
    if (ctx.ipAddress.startsWith('10.') || ctx.ipAddress.startsWith('192.168.')) {
      // Local development safe
    }

    score = Math.min(100, score);

    let riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' = 'LOW';
    let action: 'ALLOW' | 'CHALLENGE_3DS' | 'MANUAL_REVIEW' | 'REJECT' = 'ALLOW';

    if (score >= 75) {
      riskLevel = 'CRITICAL';
      action = 'REJECT';
    } else if (score >= 50) {
      riskLevel = 'HIGH';
      action = 'MANUAL_REVIEW';
    } else if (score >= 25) {
      riskLevel = 'MEDIUM';
      action = 'CHALLENGE_3DS';
    }

    return {
      score,
      riskLevel,
      action,
      flaggedRules
    };
  }
}
