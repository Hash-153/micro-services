export interface BankStatementEntry {
  entryReference: string;
  amountCents: number;
  creditDebitIndicator: 'CRDT' | 'DBIT';
  bookingDate: Date;
  valueDate: Date;
  proprietaryCode: string;
  remittanceText?: string;
}

export class Iso20022Camt053Parser {
  public static parseStatementEntries(xmlStatement: string): BankStatementEntry[] {
    const entries: BankStatementEntry[] = [];
    const entryBlocks = xmlStatement.split('<Ntry>');

    for (let i = 1; i < entryBlocks.length; i++) {
      const block = entryBlocks[i].split('</Ntry>')[0];
      const amtMatch = block.match(/<Amt[^>]*>([0-9.]+)<\/Amt>/);
      const cdtDbtMatch = block.match(/<CdtDbtInd>([A-Z]+)<\/CdtDbtInd>/);
      const refMatch = block.match(/<AcctSvcrRef>([^<]+)<\/AcctSvcrRef>/);

      if (amtMatch && cdtDbtMatch) {
        entries.push({
          entryReference: refMatch ? refMatch[1] : `REF-${i}`,
          amountCents: Math.round(parseFloat(amtMatch[1]) * 100),
          creditDebitIndicator: cdtDbtMatch[1] as 'CRDT' | 'DBIT',
          bookingDate: new Date(),
          valueDate: new Date(),
          proprietaryCode: 'NTRF'
        });
      }
    }

    return entries;
  }
}
