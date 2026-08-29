export interface CarrierZoneRateSheet {
  carrier: 'FEDEX' | 'UPS' | 'DHL' | 'USPS';
  serviceLevel: string;
  zoneRates: { zone: number; baseRateCents: number; perPoundRateCents: number }[];
}

export const CARRIER_ZONE_RATE_SHEETS: CarrierZoneRateSheet[] = [
  {
    carrier: 'FEDEX',
    serviceLevel: 'GROUND',
    zoneRates: [
      { zone: 2, baseRateCents: 850, perPoundRateCents: 65 },
      { zone: 3, baseRateCents: 920, perPoundRateCents: 75 },
      { zone: 4, baseRateCents: 980, perPoundRateCents: 85 },
      { zone: 5, baseRateCents: 1050, perPoundRateCents: 95 },
      { zone: 6, baseRateCents: 1120, perPoundRateCents: 105 },
      { zone: 7, baseRateCents: 1190, perPoundRateCents: 115 },
      { zone: 8, baseRateCents: 1260, perPoundRateCents: 125 }
    ]
  },
  {
    carrier: 'FEDEX',
    serviceLevel: 'PRIORITY_OVERNIGHT',
    zoneRates: [
      { zone: 2, baseRateCents: 2450, perPoundRateCents: 180 },
      { zone: 3, baseRateCents: 2650, perPoundRateCents: 195 },
      { zone: 4, baseRateCents: 2850, perPoundRateCents: 210 },
      { zone: 5, baseRateCents: 3100, perPoundRateCents: 230 },
      { zone: 6, baseRateCents: 3350, perPoundRateCents: 250 },
      { zone: 7, baseRateCents: 3600, perPoundRateCents: 270 },
      { zone: 8, baseRateCents: 3850, perPoundRateCents: 290 }
    ]
  },
  {
    carrier: 'UPS',
    serviceLevel: 'GROUND',
    zoneRates: [
      { zone: 2, baseRateCents: 830, perPoundRateCents: 62 },
      { zone: 3, baseRateCents: 895, perPoundRateCents: 72 },
      { zone: 4, baseRateCents: 960, perPoundRateCents: 82 },
      { zone: 5, baseRateCents: 1030, perPoundRateCents: 92 },
      { zone: 6, baseRateCents: 1100, perPoundRateCents: 102 },
      { zone: 7, baseRateCents: 1175, perPoundRateCents: 112 },
      { zone: 8, baseRateCents: 1245, perPoundRateCents: 122 }
    ]
  },
  {
    carrier: 'UPS',
    serviceLevel: 'NEXT_DAY_AIR',
    zoneRates: [
      { zone: 2, baseRateCents: 2380, perPoundRateCents: 175 },
      { zone: 3, baseRateCents: 2580, perPoundRateCents: 190 },
      { zone: 4, baseRateCents: 2780, perPoundRateCents: 205 },
      { zone: 5, baseRateCents: 3020, perPoundRateCents: 225 },
      { zone: 6, baseRateCents: 3280, perPoundRateCents: 245 },
      { zone: 7, baseRateCents: 3520, perPoundRateCents: 265 },
      { zone: 8, baseRateCents: 3780, perPoundRateCents: 285 }
    ]
  }
];

export class CarrierZonePricingEngine {
  public static calculateShippingCost(
    carrier: 'FEDEX' | 'UPS',
    serviceLevel: string,
    zone: number,
    weightPounds: number
  ): number {
    const sheet = CARRIER_ZONE_RATE_SHEETS.find(s => s.carrier === carrier && s.serviceLevel === serviceLevel);
    if (!sheet) return 1500; // Default fallback $15.00

    const zoneRate = sheet.zoneRates.find(z => z.zone === zone) || sheet.zoneRates[sheet.zoneRates.length - 1];
    const billableWeight = Math.max(1, Math.ceil(weightPounds));
    const extraPounds = Math.max(0, billableWeight - 1);

    return zoneRate.baseRateCents + extraPounds * zoneRate.perPoundRateCents;
  }
}
