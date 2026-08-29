export type IsoTransactionType = 'PURCHASE' | 'REFUND' | 'CASH_WITHDRAWAL' | 'BALANCE_INQUIRY';
export type IsoAccountType = 'DEFAULT' | 'SAVINGS' | 'CHECKING' | 'CREDIT';

export class Iso8583ProcessingCodeFormatter {
  private static readonly TXN_MAP: Record<IsoTransactionType, string> = {
    PURCHASE: '00',
    CASH_WITHDRAWAL: '01',
    REFUND: '20',
    BALANCE_INQUIRY: '30'
  };

  private static readonly ACCT_MAP: Record<IsoAccountType, string> = {
    DEFAULT: '00',
    SAVINGS: '10',
    CHECKING: '20',
    CREDIT: '30'
  };

  public static formatProcessingCode(txnType: IsoTransactionType, fromAccount: IsoAccountType = 'DEFAULT', toAccount: IsoAccountType = 'DEFAULT'): string {
    const txn = this.TXN_MAP[txnType] || '00';
    const from = this.ACCT_MAP[fromAccount] || '00';
    const to = this.ACCT_MAP[toAccount] || '00';
    return `${txn}${from}${to}`;
  }
}
