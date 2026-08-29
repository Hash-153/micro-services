export interface AntennaLocation {
  antennaId: number;
  xMeters: number;
  yMeters: number;
  zMeters: number;
}

export interface AntennaSignalReading {
  antennaId: number;
  rssiDbm: number;
}

export class RfidTriangulationEngine {
  public static estimatePosition(readings: AntennaSignalReading[], antennaLocations: AntennaLocation[]): { x: number; y: number; confidenceScore: number } {
    if (readings.length === 0) return { x: 0, y: 0, confidenceScore: 0 };

    let totalWeight = 0;
    let weightedX = 0;
    let weightedY = 0;

    for (const r of readings) {
      const loc = antennaLocations.find(a => a.antennaId === r.antennaId);
      if (loc) {
        // Convert dBm to linear power weight: 10^(rssi/10)
        const weight = Math.pow(10, (r.rssiDbm + 100) / 20);
        weightedX += loc.xMeters * weight;
        weightedY += loc.yMeters * weight;
        totalWeight += weight;
      }
    }

    if (totalWeight === 0) return { x: 0, y: 0, confidenceScore: 0 };

    return {
      x: Math.round((weightedX / totalWeight) * 100) / 100,
      y: Math.round((weightedY / totalWeight) * 100) / 100,
      confidenceScore: Math.min(1.0, readings.length / 4)
    };
  }
}
