import { InMemoryBaseRepository } from '@novacommerce/core-database';
import { PaymentTransactionEntity, LedgerJournalEntryEntity } from '@novacommerce/core-types';

export class InMemoryPaymentRepository extends InMemoryBaseRepository<PaymentTransactionEntity> {}
export class InMemoryLedgerRepository extends InMemoryBaseRepository<LedgerJournalEntryEntity> {}
