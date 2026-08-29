import { DoubleEntryLedgerEngine } from '../src/domain/double-entry-ledger.js';
import { LedgerLineEntity } from '@novacommerce/core-types';

describe('Payment Service: Double-Entry Ledger Mathematical Invariance Suite', () => {
  it('should approve balanced journal entries (Sum Debits == Sum Credits)', () => {
    const balancedLines: LedgerLineEntity[] = [
      { id: '1', journalEntryId: 'j1', accountId: '1010', entryType: 'DEBIT', amount: 15000 },
      { id: '2', journalEntryId: 'j1', accountId: '4010', entryType: 'CREDIT', amount: 12500 },
      { id: '3', journalEntryId: 'j1', accountId: '2020', entryType: 'CREDIT', amount: 2500 }
    ];

    expect(() => DoubleEntryLedgerEngine.validateBalancedEntry(balancedLines)).not.toThrow();
  });

  it('should throw error on unbalanced journal entry', () => {
    const unbalancedLines: LedgerLineEntity[] = [
      { id: '1', journalEntryId: 'j2', accountId: '1010', entryType: 'DEBIT', amount: 15000 },
      { id: '2', journalEntryId: 'j2', accountId: '4010', entryType: 'CREDIT', amount: 10000 } // missing 5000!
    ];

    expect(() => DoubleEntryLedgerEngine.validateBalancedEntry(unbalancedLines)).toThrow(/out of balance/);
  });
});
