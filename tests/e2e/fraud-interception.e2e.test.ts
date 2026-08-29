import { FraudDetector } from '../../services/payment-service/src/domain/fraud-detector.js';

describe('E2E Scenario: High-Risk Transaction Fraud Interception & 3DS Challenge', () => {
  it('should challenge 3DS on medium risk score', () => {
    const risk = FraudDetector.evaluateRisk({
      userId: 'usr-medium-risk',
      orderId: 'ord-3ds-01',
      amountCents: 600000, // $6,000 -> flags high ticket value (+25)
      currency: 'USD',
      ipAddress: '192.168.1.1',
      cardBin: '411111',
      cardCountry: 'US',
      billingCountry: 'US',
      shippingCountry: 'US',
      deviceFingerprint: 'fp_known',
      accountAgeDays: 30,
      previousOrderCount: 5,
      previousDisputeCount: 0
    });

    expect(risk.score).toBeGreaterThanOrEqual(25);
    expect(risk.action).toBe('CHALLENGE_3DS');
  });
});
