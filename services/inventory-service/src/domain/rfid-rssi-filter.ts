export interface RawRfidRead {
  epcTag: string;
  antennaId: number;
  rssiDecibels: number;
  timestamp: number;
}

export class RfidRssiFilter {
  public static filterMovingTag(reads: RawRfidRead[], minRssi: number = -65, minReadCount: number = 3): RawRfidRead[] {
    const grouped = new Map<string, RawRfidRead[]>();

    for (const r of reads) {
      if (r.rssiDecibels >= minRssi) {
        if (!grouped.has(r.epcTag)) {
          grouped.set(r.epcTag, []);
        }
        grouped.get(r.epcTag)!.push(r);
      }
    }

    const confirmed: RawRfidRead[] = [];
    for (const [tag, tagReads] of grouped.entries()) {
      if (tagReads.length >= minReadCount) {
        // Return latest read
        confirmed.push(tagReads[tagReads.length - 1]);
      }
    }

    return confirmed;
  }
}
