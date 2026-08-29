import { PaymentStatus, PaymentMethodType, PaymentGatewayProvider } from '../enums/PaymentStatus.js';
import { Money } from '../enums/Currency.js';

export interface PaymentTransactionEntity {
  id: string;
  transactionReference: string;
  orderId: string;
  userId: string;
  amount: Money;
  status: PaymentStatus;
  methodType: PaymentMethodType;
  provider: PaymentGatewayProvider;
  providerTransactionId?: string;
  failureReason?: string;
  idempotencyKey: string;
  metadata: Record<string, unknown>;
  createdAt: Date;
  updatedAt: Date;
}

export interface LedgerAccountEntity {
  id: string;
  accountNumber: string;
  name: string;
  type: 'ASSET' | 'LIABILITY' | 'EQUITY' | 'REVENUE' | 'EXPENSE';
  currency: string;
  balance: number; // in cents
  createdAt: Date;
  updatedAt: Date;
}

export interface LedgerJournalEntryEntity {
  id: string;
  entryNumber: string;
  description: string;
  transactionId?: string;
  referenceType: string;
  referenceId: string;
  postedAt: Date;
  lines: LedgerLineEntity[];
}

export interface LedgerLineEntity {
  id: string;
  journalEntryId: string;
  accountId: string;
  entryType: 'DEBIT' | 'CREDIT';
  amount: number; // in cents
  memo?: string;
}
