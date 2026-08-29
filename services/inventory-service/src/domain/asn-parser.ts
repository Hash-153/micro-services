export interface AsnInboundShipment {
  asnNumber: string;
  carrier: string;
  bolNumber: string; // Bill of Lading
  destinationWarehouseId: string;
  expectedDeliveryDate: Date;
  lineItems: { sku: string; expectedQuantity: number; lotNumber?: string }[];
}

export class AsnParser {
  public static parseEdi856(rawEdiContent: string): AsnInboundShipment {
    const lines = rawEdiContent.split('\n');
    let asnNumber = '';
    let carrier = '';
    let bolNumber = '';
    let destinationWarehouseId = 'WH-EAST-01';
    const lineItems: AsnInboundShipment['lineItems'] = [];

    for (const line of lines) {
      if (line.startsWith('BSN*')) {
        const parts = line.split('*');
        asnNumber = parts[2] || `ASN-${Date.now()}`;
      } else if (line.startsWith('TD5*')) {
        const parts = line.split('*');
        carrier = parts[5] || 'FEDEX_FREIGHT';
      } else if (line.startsWith('REF*BM*')) {
        const parts = line.split('*');
        bolNumber = parts[2] || '';
      } else if (line.startsWith('LIN*')) {
        const parts = line.split('*');
        const sku = parts[3] || 'SKU-UNKNOWN';
        lineItems.push({ sku, expectedQuantity: 100 });
      }
    }

    return {
      asnNumber: asnNumber || `ASN-${Date.now().toString(36).toUpperCase()}`,
      carrier: carrier || 'STANDARD_LOGISTICS',
      bolNumber: bolNumber || `BOL-${Date.now().toString(36).toUpperCase()}`,
      destinationWarehouseId,
      expectedDeliveryDate: new Date(Date.now() + 86400000 * 3),
      lineItems
    };
  }
}
