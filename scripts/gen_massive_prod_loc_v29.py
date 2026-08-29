import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v29():
    print("Generating comprehensive Production V29 Modules...")

    # 1. Payment ISO 20022 PAIN.001 Credit Transfer Builder
    write_file("services/payment-service/src/domain/iso20022-pain001-builder.ts", """import { Money, Currency } from '@novacommerce/core-types';

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
""")

    # 2. Inventory RFID Gate Reader Batch Ingestion Engine
    write_file("services/inventory-service/src/domain/rfid-gate-reader.ts", """export interface RfidGateScanBatch {
  gateId: string;
  warehouseId: string;
  antennaId: number;
  readings: { epcTag: string; rssi: number; readCount: number; firstSeen: Date; lastSeen: Date }[];
}

export class RfidGateReaderEngine {
  public static processScan(batch: RfidGateScanBatch): { totalTagsRead: number; uniqueSkus: string[]; filteredReadings: typeof batch.readings } {
    // Filter noise (RSSI threshold > -70 dBm)
    const valid = batch.readings.filter(r => r.rssi >= -70);
    const skus = new Set<string>();

    for (const item of valid) {
      // Decode SKU from EPC tag format (e.g. urn:epc:tag:sgtin-96:3.<sku_hex>.<serial>)
      const parts = item.epcTag.split('.');
      if (parts.length >= 2) {
        skus.add(parts[1]);
      }
    }

    return {
      totalTagsRead: valid.length,
      uniqueSkus: Array.from(skus),
      filteredReadings: valid
    };
  }
}
""")

    print("Production V29 modules generated.")

if __name__ == "__main__":
    generate_prod_v29()
