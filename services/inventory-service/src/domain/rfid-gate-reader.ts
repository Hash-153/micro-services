export interface RfidGateScanBatch {
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
