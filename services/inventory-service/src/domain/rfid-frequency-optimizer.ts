export interface RfidFrequencyBandConfig {
  region: 'US_FCC' | 'EU_ETSI' | 'JP_TELEC';
  minFrequencyMhz: number;
  maxFrequencyMhz: number;
  channelHopCount: number;
  maxTxPowerEirpDbm: number;
}

export const RFID_REGIONAL_BANDS: Record<string, RfidFrequencyBandConfig> = {
  US_FCC: { region: 'US_FCC', minFrequencyMhz: 902.0, maxFrequencyMhz: 928.0, channelHopCount: 50, maxTxPowerEirpDbm: 36.0 },
  EU_ETSI: { region: 'EU_ETSI', minFrequencyMhz: 865.0, maxFrequencyMhz: 868.0, channelHopCount: 4, maxTxPowerEirpDbm: 33.0 },
  JP_TELEC: { region: 'JP_TELEC', minFrequencyMhz: 916.8, maxFrequencyMhz: 923.4, channelHopCount: 6, maxTxPowerEirpDbm: 36.0 }
};

export class RfidFrequencyOptimizer {
  public static getOptimalBand(regionCode: string = 'US_FCC'): RfidFrequencyBandConfig {
    return RFID_REGIONAL_BANDS[regionCode] || RFID_REGIONAL_BANDS.US_FCC;
  }
}
