import { LedgerLineEntity, Currency } from '@novacommerce/core-types';

export interface ReclassificationEntry {
  originalLineId: string;
  fromAccountId: string;
  toAccountId: string;
  amountCents: number;
  reason: string;
  effectiveDate: Date;
}

export class LedgerReclassificationEngine {
  public static createReclassificationLines(
    entry: ReclassificationEntry,
    journalEntryId: string = crypto.randomUUID()
  ): LedgerLineEntity[] {
    return [
      // Credit original account to reverse
      {
        id: crypto.randomUUID(),
        journalEntryId,
        accountId: entry.fromAccountId,
        entryType: 'CREDIT',
        amount: entry.amountCents,
        memo: `Reclassification reversal: ${entry.reason}`
      },
      // Debit new target account
      {
        id: crypto.randomUUID(),
        journalEntryId,
        accountId: entry.toAccountId,
        entryType: 'DEBIT',
        amount: entry.amountCents,
        memo: `Reclassified into account: ${entry.reason}`
      }
    ];
  }
}
