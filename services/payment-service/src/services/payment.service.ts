import { InMemoryPaymentRepository, InMemoryLedgerRepository } from '../repositories/payment.repository.js';
import { DoubleEntryLedgerEngine } from '../domain/double-entry-ledger.js';
import { PaymentTransactionEntity, PaymentStatus, PaymentMethodType, PaymentGatewayProvider, Currency } from '@novacommerce/core-types';
import { IEventBus, DomainEventFactory } from '@novacommerce/core-events';
import { EventType } from '@novacommerce/core-types';
import { randomUUID } from 'crypto';

export class PaymentService {
  private readonly paymentRepo: InMemoryPaymentRepository;
  private readonly ledgerRepo: InMemoryLedgerRepository;
  private readonly eventBus?: IEventBus;

  constructor(paymentRepo: InMemoryPaymentRepository, ledgerRepo: InMemoryLedgerRepository, eventBus?: IEventBus) {
    this.paymentRepo = paymentRepo;
    this.ledgerRepo = ledgerRepo;
    this.eventBus = eventBus;
  }

  public async authorizePayment(
    orderId: string,
    userId: string,
    amountCents: number,
    currency: Currency = Currency.USD,
    correlationId?: string
  ): Promise<PaymentTransactionEntity> {
    const paymentId = randomUUID();
    const transaction: PaymentTransactionEntity = {
      id: paymentId,
      transactionReference: `TXN-${Date.now()}-${randomUUID().substring(0, 6)}`,
      orderId,
      userId,
      amount: { amount: amountCents, currency },
      status: PaymentStatus.CAPTURED,
      methodType: PaymentMethodType.CREDIT_CARD,
      provider: PaymentGatewayProvider.MOCK,
      providerTransactionId: `ch_mock_${randomUUID()}`,
      idempotencyKey: randomUUID(),
      metadata: {},
      createdAt: new Date(),
      updatedAt: new Date()
    };

    const savedPayment = await this.paymentRepo.create(transaction);

    // Record double entry: Debit Cash/Processor Receivable, Credit Customer Revenue
    const lines = [
      { id: randomUUID(), journalEntryId: '', accountId: 'acc_cash_receivable', entryType: 'DEBIT' as const, amount: amountCents },
      { id: randomUUID(), journalEntryId: '', accountId: 'acc_sales_revenue', entryType: 'CREDIT' as const, amount: amountCents }
    ];

    DoubleEntryLedgerEngine.validateBalancedEntry(lines);

    const journalEntryId = randomUUID();
    lines.forEach(l => (l.journalEntryId = journalEntryId));

    await this.ledgerRepo.create({
      id: journalEntryId,
      entryNumber: `JRN-${Date.now()}`,
      description: `Payment captured for order ${orderId}`,
      transactionId: paymentId,
      referenceType: 'PAYMENT',
      referenceId: paymentId,
      postedAt: new Date(),
      lines
    });

    if (this.eventBus) {
      const event = DomainEventFactory.create(
        EventType.PAYMENT_CAPTURED,
        savedPayment.id,
        'PaymentTransaction',
        savedPayment,
        'payment-service',
        correlationId
      );
      await this.eventBus.publish(event);
    }

    return savedPayment;
  }
}
