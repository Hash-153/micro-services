import { PaymentTransactionEntity, Currency } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export interface DisputeRecord {
  disputeId: string;
  transactionReference: string;
  amountCents: number;
  currency: Currency;
  reasonCode: string;
  evidenceDueBy: Date;
  status: 'NEEDS_RESPONSE' | 'UNDER_REVIEW' | 'WON' | 'LOST';
  submittedEvidenceUrls: string[];
  createdAt: Date;
}

export class DisputeManager {
  private logger: Logger;
  private disputes: Map<string, DisputeRecord> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public registerDispute(
    transactionRef: string,
    amountCents: number,
    currency: Currency,
    reasonCode: string,
    evidenceDueDays: number = 7
  ): DisputeRecord {
    const disputeId = `dp_${Date.now().toString(36)}`;
    const evidenceDueBy = new Date(Date.now() + evidenceDueDays * 86400000);

    const dispute: DisputeRecord = {
      disputeId,
      transactionReference: transactionRef,
      amountCents,
      currency,
      reasonCode,
      evidenceDueBy,
      status: 'NEEDS_RESPONSE',
      submittedEvidenceUrls: [],
      createdAt: new Date()
    };

    this.disputes.set(disputeId, dispute);
    this.logger.warn(`Payment dispute received: ${disputeId} for txn ${transactionRef} ($${(amountCents / 100).toFixed(2)})`);
    return dispute;
  }

  public submitEvidence(disputeId: string, evidenceUrls: string[]): DisputeRecord {
    const dispute = this.disputes.get(disputeId);
    if (!dispute) throw new Error(`Dispute ${disputeId} not found`);

    dispute.submittedEvidenceUrls.push(...evidenceUrls);
    dispute.status = 'UNDER_REVIEW';

    this.logger.info(`Evidence submitted for dispute ${disputeId} (${evidenceUrls.length} documents)`);
    return dispute;
  }
}
