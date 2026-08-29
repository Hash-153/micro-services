export interface PixQrCodePayload {
  payloadFormatIndicator: '01';
  pointOfInitiationMethod: '12'; // Dynamic QR code
  merchantAccountInfo: {
    gui: 'br.gov.bcb.pix';
    pixKey: string;
    description: string;
  };
  merchantCategoryCode: '0000';
  transactionCurrency: '986'; // BRL ISO 4217
  transactionAmount: string;
  countryCode: 'BR';
  merchantName: string;
  merchantCity: string;
  additionalDataField: {
    txId: string;
  };
}

export class PixPaymentEngine {
  public static generateDynamicPixPayload(
    pixKey: string,
    txId: string,
    amountBrl: number,
    merchantName: string = 'NOVA COMMERCE BR',
    merchantCity: string = 'SAO PAULO'
  ): string {
    const formattedAmount = amountBrl.toFixed(2);
    // Standard EMVCo QR code string generation for Brazilian Central Bank Pix
    const guiField = `0014br.gov.bcb.pix01${pixKey.length.toString().padStart(2, '0')}${pixKey}`;
    const accountInfo = `26${guiField.length.toString().padStart(2, '0')}${guiField}`;
    const txField = `05${txId.length.toString().padStart(2, '0')}${txId}`;
    const additionalData = `62${txField.length.toString().padStart(2, '0')}${txField}`;

    const rawPayload = `000201010212${accountInfo}52040000530398654${formattedAmount.length.toString().padStart(2, '0')}${formattedAmount}5802BR59${merchantName.length.toString().padStart(2, '0')}${merchantName}60${merchantCity.length.toString().padStart(2, '0')}${merchantCity}${additionalData}6304`;

    // Calculate CRC16-CCITT (0xFFFF)
    const crc = this.computeCrc16(rawPayload);
    return `${rawPayload}${crc}`;
  }

  private static computeCrc16(payload: string): string {
    let crc = 0xFFFF;
    for (let i = 0; i < payload.length; i++) {
      crc ^= payload.charCodeAt(i) << 8;
      for (let j = 0; j < 8; j++) {
        if ((crc & 0x8000) !== 0) {
          crc = ((crc << 1) ^ 0x1021) & 0xFFFF;
        } else {
          crc = (crc << 1) & 0xFFFF;
        }
      }
    }
    return crc.toString(16).toUpperCase().padStart(4, '0');
  }
}
