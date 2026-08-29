import { LedgerJournalEntryEntity, LedgerLineEntity, AppError, ErrorCode } from '@novacommerce/core-types';

export class DoubleEntryLedgerEngine {
  public static validateBalancedEntry(lines: LedgerLineEntity[]): void {
    let totalDebit = 0;
    let totalCredit = 0;

    for (const line of lines) {
      if (line.entryType === 'DEBIT') {
        totalDebit += line.amount;
      } else if (line.entryType === 'CREDIT') {
        totalCredit += line.amount;
      }
    }

    if (totalDebit !== totalCredit) {
      throw new AppError(
        `Double-entry ledger is out of balance! Debits (${totalDebit}) do not equal Credits (${totalCredit})`,
        400,
        ErrorCode.LEDGER_UNBALANCED_ENTRY
      );
    }
  }
}
