export interface Iso8583BitmapFields {
  mti: string; // e.g. "0100", "0110", "0200", "0210"
  pan?: string; // Field 2
  processingCode?: string; // Field 3
  amountCents?: number; // Field 4
  transmissionDateTime?: string; // Field 7
  stan?: string; // Field 11
  localTransactionTime?: string; // Field 12
  localTransactionDate?: string; // Field 13
  posEntryMode?: string; // Field 22
  cardSequenceNumber?: string; // Field 23
  functionCode?: string; // Field 24
  retrievalReferenceNumber?: string; // Field 37
  authorizationIdResponse?: string; // Field 38
  responseCode?: string; // Field 39
}

export class Iso8583MessageCodec {
  public static encode(fields: Iso8583BitmapFields): string {
    const parts: string[] = [fields.mti];

    // Encode Fields
    if (fields.pan) parts.push(`02${fields.pan.length.toString().padStart(2, '0')}${fields.pan}`);
    if (fields.processingCode) parts.push(`03${fields.processingCode}`);
    if (fields.amountCents !== undefined) parts.push(`04${fields.amountCents.toString().padStart(12, '0')}`);
    if (fields.stan) parts.push(`11${fields.stan.padStart(6, '0')}`);
    if (fields.retrievalReferenceNumber) parts.push(`37${fields.retrievalReferenceNumber.padStart(12, '0')}`);
    if (fields.responseCode) parts.push(`39${fields.responseCode.padStart(2, '0')}`);

    return parts.join('|');
  }

  public static decode(rawMessage: string): Iso8583BitmapFields {
    const parts = rawMessage.split('|');
    const fields: Iso8583BitmapFields = { mti: parts[0] || '0100' };

    for (let i = 1; i < parts.length; i++) {
      const chunk = parts[i];
      const fieldNum = chunk.slice(0, 2);
      const val = chunk.slice(2);

      if (fieldNum === '03') fields.processingCode = val;
      if (fieldNum === '04') fields.amountCents = parseInt(val, 10);
      if (fieldNum === '11') fields.stan = val;
      if (fieldNum === '37') fields.retrievalReferenceNumber = val;
      if (fieldNum === '39') fields.responseCode = val;
    }

    return fields;
  }
}
