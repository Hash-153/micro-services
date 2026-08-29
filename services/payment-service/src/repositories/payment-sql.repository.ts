import { PaymentTransactionEntity, PaymentStatus, PaginationParams, PaginatedResult } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export class PaymentSqlRepository {
  private logger: Logger;
  private transactions: Map<string, PaymentTransactionEntity> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async findById(id: string): Promise<PaymentTransactionEntity | null> {
    return this.transactions.get(id) || null;
  }

  public async findByReference(ref: string): Promise<PaymentTransactionEntity | null> {
    for (const txn of this.transactions.values()) {
      if (txn.transactionReference === ref) return txn;
    }
    return null;
  }

  public async create(txn: PaymentTransactionEntity): Promise<PaymentTransactionEntity> {
    this.transactions.set(txn.id, txn);
    this.logger.info(`Payment transaction persisted: ${txn.transactionReference} ($${(txn.amount.amount / 100).toFixed(2)})`);
    return txn;
  }

  public async updateStatus(id: string, status: PaymentStatus, failureReason?: string): Promise<PaymentTransactionEntity> {
    const txn = this.transactions.get(id);
    if (!txn) throw new Error(`Payment transaction ${id} not found`);
    txn.status = status;
    if (failureReason) txn.failureReason = failureReason;
    txn.updatedAt = new Date();
    this.transactions.set(id, txn);
    return txn;
  }
}
