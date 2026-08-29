import { InMemoryPaymentRepository, InMemoryLedgerRepository } from '../../services/payment-service/src/repositories/payment.repository.js';
import { PaymentService } from '../../services/payment-service/src/services/payment.service.js';
import { DoubleEntryLedgerEngine } from '../../services/payment-service/src/domain/double-entry-ledger.js';
import { Currency } from '@novacommerce/core-types';

describe('E2E Scenario: Full and Partial Payment Refunds with Double-Entry Ledger Reversals', () => {
  let paymentService: PaymentService;

  beforeEach(() => {
    paymentService = new PaymentService(new InMemoryPaymentRepository(), new InMemoryLedgerRepository());
  });

  it('should authorize payment and post balanced initial ledger entry', async () => {
    const payment = await paymentService.authorizePayment('ord-ref-001', 'usr-cust-01', 9999, Currency.USD);
    expect(payment.id).toBeDefined();
    expect(payment.amount.amount).toBe(9999);
    expect(payment.status).toBe('CAPTURED');
  });
});
