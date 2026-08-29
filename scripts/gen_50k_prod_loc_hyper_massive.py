import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_hyper_massive():
    print("Generating comprehensive Production Hyper Massive Modules...")

    # 1. Carrier Zone Pricing Sheets Matrix
    rate_sheets_code = """export interface CarrierZoneRateSheet {
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
"""
    write_file("services/fulfillment-service/src/domain/carrier-zone-pricing.ts", rate_sheets_code)

    # 2. Analytics Standard KPI Aggregator
    write_file("services/analytics-service/src/domain/standard-kpi-aggregator.ts", """import { OrderEntity } from '@novacommerce/core-types';

export interface EnterpriseKpiSummary {
  periodDate: string;
  grossMerchandiseValueCents: number;
  netRevenueCents: number;
  totalOrdersCount: number;
  averageOrderValueCents: number;
  unitsPerOrder: number;
  totalDiscountAmountCents: number;
  totalRefundAmountCents: number;
  refundRatePercent: number;
}

export class StandardKpiAggregator {
  public static aggregateDailyKpis(orders: OrderEntity[], periodDate: string = new Date().toISOString().slice(0, 10)): EnterpriseKpiSummary {
    const validOrders = orders.filter(o => o.status !== 'CANCELLED');
    const refundedOrders = orders.filter(o => o.status === 'REFUNDED' || o.status === 'PARTIALLY_REFUNDED');

    const gmv = orders.reduce((acc, o) => acc + o.totalAmount.amount, 0);
    const discounts = orders.reduce((acc, o) => acc + o.discountAmount.amount, 0);
    const refunds = refundedOrders.reduce((acc, o) => acc + o.totalAmount.amount, 0);
    const netRevenue = Math.max(0, gmv - discounts - refunds);

    const totalUnits = validOrders.reduce((acc, o) => acc + o.items.reduce((sum, it) => sum + it.quantity, 0), 0);
    const aov = validOrders.length > 0 ? Math.round(gmv / validOrders.length) : 0;
    const unitsPerOrder = validOrders.length > 0 ? Math.round((totalUnits / validOrders.length) * 10) / 10 : 0;
    const refundRate = gmv > 0 ? (refunds / gmv) * 100 : 0;

    return {
      periodDate,
      grossMerchandiseValueCents: gmv,
      netRevenueCents: netRevenue,
      totalOrdersCount: validOrders.length,
      averageOrderValueCents: aov,
      unitsPerOrder,
      totalDiscountAmountCents: discounts,
      totalRefundAmountCents: refunds,
      refundRatePercent: Math.round(refundRate * 10) / 10
    };
  }
}
""")

    print("Production hyper massive modules generated.")

if __name__ == "__main__":
    generate_prod_hyper_massive()
