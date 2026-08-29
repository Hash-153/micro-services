import { FraudDetector } from '../../services/payment-service/src/domain/fraud-detector.js';

describe('E2E Scenario: Payment 3D-Secure Fraud Challenge Evaluation', () => {
  it('should pass low risk transactions with zero friction', () => {
    const lowRisk = FraudDetector.evaluateRisk({
      userId: 'usr-vip-001',
      orderId: 'ord-low-risk-001',
      amountCents: 4500, // $45.00
      currency: 'USD',
      ipAddress: '192.168.1.100',
      cardBin: '411111',
      cardCountry: 'US',
      billingCountry: 'US',
      shippingCountry: 'US',
      deviceFingerprint: 'fp_known_device',
      accountAgeDays: 365,
      previousOrderCount: 42,
      previousDisputeCount: 0
    });

    expect(lowRisk.score).toBeLessThan(25);
    expect(lowRisk.action).toBe('ALLOW');
    expect(lowRisk.factors.length).toBe(0);
  });

  it('should decline high risk transactions immediately', () => {
    const highRisk = FraudDetector.evaluateRisk({
      userId: 'usr-suspicious-01',
      orderId: 'ord-high-risk-001',
      amountCents: 1500000, // $15,000.00 (+25)
      currency: 'USD',
      ipAddress: '10.0.0.1',
      cardBin: '424242',
      cardCountry: 'US',
      billingCountry: 'US',
      shippingCountry: 'NG', // Country mismatch (+30)
      deviceFingerprint: 'fp_new',
      accountAgeDays: 0, // Brand new account (+15)
      previousOrderCount: 0,
      previousDisputeCount: 2 // Previous disputes (+40) -> Total = 110 >= 70
    });

    expect(highRisk.score).toBeGreaterThanOrEqual(70);
    expect(highRisk.action).toBe('BLOCK');
  });
});
