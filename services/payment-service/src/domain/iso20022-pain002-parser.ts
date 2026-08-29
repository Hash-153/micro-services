export interface PaymentStatusReport {
  originalMessageId: string;
  originalInstructionId: string;
  transactionStatus: 'ACTC' | 'ACCP' | 'RJCT' | 'PDNG';
  reasonCode?: string;
  additionalInfo?: string;
}

export class Iso20022Pain002Parser {
  public static parseStatusReport(xmlContent: string): PaymentStatusReport {
    const msgIdMatch = xmlContent.match(/<OrgnlMsgId>([^<]+)<\/OrgnlMsgId>/);
    const instrIdMatch = xmlContent.match(/<OrgnlInstrId>([^<]+)<\/OrgnlInstrId>/);
    const statusMatch = xmlContent.match(/<TxSts>([A-Z]+)<\/TxSts>/);
    const rsnMatch = xmlContent.match(/<Cd>([A-Z0-9]+)<\/Cd>/);

    return {
      originalMessageId: msgIdMatch ? msgIdMatch[1] : 'UNKNOWN_MSG',
      originalInstructionId: instrIdMatch ? instrIdMatch[1] : 'UNKNOWN_INSTR',
      transactionStatus: (statusMatch ? statusMatch[1] : 'PDNG') as PaymentStatusReport['transactionStatus'],
      reasonCode: rsnMatch ? rsnMatch[1] : undefined
    };
  }
}
