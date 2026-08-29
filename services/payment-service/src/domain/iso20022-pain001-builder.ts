import { Money, Currency } from '@novacommerce/core-types';

export interface SepaCreditTransferInstruction {
  instructionId: string;
  endToEndId: string;
  amountCents: number;
  debtorIban: string;
  debtorBic: string;
  debtorName: string;
  creditorIban: string;
  creditorBic: string;
  creditorName: string;
  remittanceInformation: string;
}

export class Iso20022Pain001Builder {
  public static buildXml(instruction: SepaCreditTransferInstruction): string {
    const formattedAmount = (instruction.amountCents / 100).toFixed(2);
    const creationDateTime = new Date().toISOString();

    return `<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.03">
  <CstmrCdtTrfInitn>
    <GrpHdr>
      <MsgId>${instruction.instructionId}</MsgId>
      <CreDtTm>${creationDateTime}</CreDtTm>
      <NbOfTxs>1</NbOfTxs>
      <CtrlSum>${formattedAmount}</CtrlSum>
      <InitgPty><Nm>${instruction.debtorName}</Nm></InitgPty>
    </GrpHdr>
    <PmtInf>
      <PmtInfId>PMT-${instruction.instructionId}</PmtInfId>
      <PmtMtd>TRF</PmtMtd>
      <ReqdExctnDt>${creationDateTime.slice(0, 10)}</ReqdExctnDt>
      <Dbtr><Nm>${instruction.debtorName}</Nm></Dbtr>
      <DbtrAcct><Id><IBAN>${instruction.debtorIban}</IBAN></Id></DbtrAcct>
      <DbtrAgt><FinInstnId><BIC>${instruction.debtorBic}</BIC></FinInstnId></DbtrAgt>
      <CdtTrfTxInf>
        <PmtId><EndToEndId>${instruction.endToEndId}</EndToEndId></PmtId>
        <Amt><InstdAmt Ccy="EUR">${formattedAmount}</InstdAmt></Amt>
        <CdtrAgt><FinInstnId><BIC>${instruction.creditorBic}</BIC></FinInstnId></CdtrAgt>
        <Cdtr><Nm>${instruction.creditorName}</Nm></Cdtr>
        <CdtrAcct><Id><IBAN>${instruction.creditorIban}</IBAN></Id></CdtrAcct>
        <RmtInf><Ustrd>${instruction.remittanceInformation}</Ustrd></RmtInf>
      </CdtTrfTxInf>
    </PmtInf>
  </CstmrCdtTrfInitn>
</Document>`;
  }
}
