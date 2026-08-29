import { LedgerLineEntity, Currency } from '@novacommerce/core-types';

export class LedgerTransactionBuilder {
  private journalEntryId: string;
  private lines: LedgerLineEntity[] = [];

  constructor(journalEntryId: string = crypto.randomUUID()) {
    this.journalEntryId = journalEntryId;
  }

  public debit(accountId: string, amountCents: number, memo?: string): this {
    if (amountCents <= 0) throw new Error('Debit amount must be strictly positive');
    this.lines.push({
      id: crypto.randomUUID(),
      journalEntryId: this.journalEntryId,
      accountId,
      entryType: 'DEBIT',
      amount: amountCents,
      memo
    });
    return this;
  }

  public credit(accountId: string, amountCents: number, memo?: string): this {
    if (amountCents <= 0) throw new Error('Credit amount must be strictly positive');
    this.lines.push({
      id: crypto.randomUUID(),
      journalEntryId: this.journalEntryId,
      accountId,
      entryType: 'CREDIT',
      amount: amountCents,
      memo
    });
    return this;
  }

  public build(): { journalEntryId: string; lines: LedgerLineEntity[]; totalDebitCents: number; totalCreditCents: number } {
    const totalDebit = this.lines.filter(l => l.entryType === 'DEBIT').reduce((acc, l) => acc + l.amount, 0);
    const totalCredit = this.lines.filter(l => l.entryType === 'CREDIT').reduce((acc, l) => acc + l.amount, 0);

    if (totalDebit !== totalCredit) {
      throw new Error(`Unbalanced double-entry journal entry: total debits ($${(totalDebit / 100).toFixed(2)}) must equal total credits ($${(totalCredit / 100).toFixed(2)})`);
    }

    return {
      journalEntryId: this.journalEntryId,
      lines: this.lines,
      totalDebitCents: totalDebit,
      totalCreditCents: totalCredit
    };
  }
}
