import { FraudDetector } from '../src/domain/fraud-detector.js';

describe('Fraud Detection Rule Engine Suite', () => {
  it('should allow low risk transaction with matching countries', () => {
    const res = FraudDetector.evaluateRisk({
      userId: 'u1',
      orderId: 'o1',
      amountCents: 4999,
      currency: 'USD',
      ipAddress: '192.168.1.1',
      cardBin: '411111',
      cardCountry: 'US',
      billingCountry: 'US',
      shippingCountry: 'US',
      deviceFingerprint: 'fp_123',
      accountAgeDays: 120,
      previousOrderCount: 15,
      previousDisputeCount: 0
    });

    expect(res.riskLevel).toBe('LOW');
    expect(res.action).toBe('ALLOW');
  });

  it('should flag critical risk on prior disputes and country mismatch', () => {
    const res = FraudDetector.evaluateRisk({
      userId: 'u2',
      orderId: 'o2',
      amountCents: 600000, // $6,000
      currency: 'USD',
      ipAddress: '203.0.113.1',
      cardBin: '411111',
      cardCountry: 'US',
      billingCountry: 'US',
      shippingCountry: 'RU',
      deviceFingerprint: 'fp_999',
      accountAgeDays: 0,
      previousOrderCount: 0,
      previousDisputeCount: 2
    });

    expect(res.riskLevel).toBe('CRITICAL');
    expect(res.action).toBe('REJECT');
    expect(res.flaggedRules).toContain('RULE_GEO_COUNTRY_MISMATCH');
    expect(res.flaggedRules).toContain('RULE_PRIOR_DISPUTE_HISTORY');
  });
});
