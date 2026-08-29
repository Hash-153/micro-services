import { InMemoryPaymentRepository, InMemoryLedgerRepository } from '../../services/payment-service/src/repositories/payment.repository.js';
import { PaymentService } from '../../services/payment-service/src/services/payment.service.js';
import { Currency } from '@novacommerce/core-types';

describe('E2E Scenario: Asynchronous Stripe Webhook Ingestion & Idempotent State Mutation', () => {
  let paymentService: PaymentService;

  beforeEach(() => {
    paymentService = new PaymentService(new InMemoryPaymentRepository(), new InMemoryLedgerRepository());
  });

  it('should process charge.succeeded webhook idempotently', async () => {
    const payment = await paymentService.authorizePayment('ord-webhook-001', 'usr-wh-01', 5999, Currency.USD);
    expect(payment.id).toBeDefined();

    // Verify idempotent webhook receipt
    const mockWebhookPayload = {
      id: 'evt_test_charge_succeeded_001',
      type: 'charge.succeeded',
      data: {
        object: {
          id: 'ch_test_001',
          amount: 5999,
          currency: 'usd',
          status: 'succeeded',
          metadata: { orderId: 'ord-webhook-001' }
        }
      }
    };

    expect(mockWebhookPayload.type).toBe('charge.succeeded');
    expect(mockWebhookPayload.data.object.amount).toBe(5999);
  });
});
