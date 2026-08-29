export interface FraudFeatures {
  transactionAmountCents: number;
  ipVelocityPerHour: number;
  cardAttemptsPerDay: number;
  isCountryMismatch: boolean;
  isProxyOrVpn: boolean;
  accountAgeDays: number;
  previousChargebackCount: number;
}

export class BayesianFraudEngine {
  public static calculateRiskProbability(features: FraudFeatures): { probability: number; riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'; recommendation: 'APPROVE' | 'CHALLENGE_3DS' | 'MANUAL_REVIEW' | 'REJECT' } {
    let priorOdds = 0.02 / (1 - 0.02); // Baseline fraud prior: 2%

    // Likelihood ratios (LR)
    const lrAmount = features.transactionAmountCents > 500000 ? 3.5 : 1.0;
    const lrIpVelocity = features.ipVelocityPerHour > 5 ? 4.2 : 1.0;
    const lrCardAttempts = features.cardAttemptsPerDay > 3 ? 5.0 : 1.0;
    const lrCountryMismatch = features.isCountryMismatch ? 3.8 : 1.0;
    const lrProxy = features.isProxyOrVpn ? 4.5 : 1.0;
    const lrAccountAge = features.accountAgeDays < 1 ? 2.5 : 0.8;
    const lrChargebacks = features.previousChargebackCount > 0 ? 10.0 : 0.9;

    const posteriorOdds = priorOdds * lrAmount * lrIpVelocity * lrCardAttempts * lrCountryMismatch * lrProxy * lrAccountAge * lrChargebacks;
    const probability = posteriorOdds / (1 + posteriorOdds);

    let riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    let recommendation: 'APPROVE' | 'CHALLENGE_3DS' | 'MANUAL_REVIEW' | 'REJECT';

    if (probability < 0.15) {
      riskLevel = 'LOW';
      recommendation = 'APPROVE';
    } else if (probability < 0.45) {
      riskLevel = 'MEDIUM';
      recommendation = 'CHALLENGE_3DS';
    } else if (probability < 0.75) {
      riskLevel = 'HIGH';
      recommendation = 'MANUAL_REVIEW';
    } else {
      riskLevel = 'CRITICAL';
      recommendation = 'REJECT';
    }

    return {
      probability: Math.round(probability * 1000) / 1000,
      riskLevel,
      recommendation
    };
  }
}
