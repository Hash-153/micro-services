import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def build_fulfillment_domain():
    print("Building Fulfillment domain expanded...")
    
    # 1. Carrier Rate Engine
    write_file("services/fulfillment-service/src/domain/carrier-rate-engine.ts", """import { CarrierCode, CarrierRateQuote, CarrierRateQuoteRequest } from '@novacommerce/core-types';

export class CarrierRateEngine {
  private static readonly BASE_RATES: Record<CarrierCode, { groundBaseCents: number; expressBaseCents: number; perKgCents: number; fuelSurchargePercent: number }> = {
    [CarrierCode.FEDEX]: { groundBaseCents: 850, expressBaseCents: 1850, perKgCents: 150, fuelSurchargePercent: 12.5 },
    [CarrierCode.UPS]: { groundBaseCents: 820, expressBaseCents: 1800, perKgCents: 145, fuelSurchargePercent: 12.0 },
    [CarrierCode.DHL]: { groundBaseCents: 1200, expressBaseCents: 2200, perKgCents: 210, fuelSurchargePercent: 15.0 },
    [CarrierCode.USPS]: { groundBaseCents: 650, expressBaseCents: 1450, perKgCents: 110, fuelSurchargePercent: 5.0 },
    [CarrierCode.INTERNAL_FLEET]: { groundBaseCents: 500, expressBaseCents: 1000, perKgCents: 80, fuelSurchargePercent: 0.0 },
    [CarrierCode.MOCK_CARRIER]: { groundBaseCents: 500, expressBaseCents: 1000, perKgCents: 50, fuelSurchargePercent: 0.0 }
  };

  public static calculateQuotes(request: CarrierRateQuoteRequest): CarrierRateQuote[] {
    const quotes: CarrierRateQuote[] = [];
    const billableWeightKg = Math.max(
      request.weightGrams / 1000,
      (request.dimensionsMm.length * request.dimensionsMm.width * request.dimensionsMm.height) / (5000 * 1000) // Dim divisor 5000
    );

    const carriers: CarrierCode[] = [CarrierCode.FEDEX, CarrierCode.UPS, CarrierCode.DHL, CarrierCode.USPS];

    for (const carrier of carriers) {
      const config = this.BASE_RATES[carrier];
      const weightCostCents = Math.round(billableWeightKg * config.perKgCents);
      const fuelMultiplier = 1 + config.fuelSurchargePercent / 100;
      const residentialSurchargeCents = request.isResidential ? 350 : 0;

      // Ground Service
      const groundTotal = Math.round((config.groundBaseCents + weightCostCents) * fuelMultiplier + residentialSurchargeCents);
      quotes.push({
        carrier,
        serviceLevel: 'GROUND',
        serviceName: `${carrier} Standard Ground`,
        rateCents: groundTotal,
        estimatedTransitDays: 3,
        guaranteedDelivery: false
      });

      // Express Service
      const expressTotal = Math.round((config.expressBaseCents + weightCostCents * 1.5) * fuelMultiplier + residentialSurchargeCents);
      quotes.push({
        carrier,
        serviceLevel: 'EXPRESS_2DAY',
        serviceName: `${carrier} 2-Day Priority Express`,
        rateCents: expressTotal,
        estimatedTransitDays: 2,
        guaranteedDelivery: true
      });
    }

    quotes.sort((a, b) => a.rateCents - b.rateCents);
    return quotes;
  }
}
""")

    # 2. Tracking Webhook Parser
    write_file("services/fulfillment-service/src/domain/tracking-webhook-parser.ts", """import { FulfillmentStatus, CarrierCode } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export interface NormalizedTrackingEvent {
  trackingNumber: string;
  carrier: CarrierCode;
  status: FulfillmentStatus;
  milestoneDescription: string;
  locationCity?: string;
  locationState?: string;
  locationCountry?: string;
  carrierStatusCode: string;
  eventTimestamp: Date;
}

export class TrackingWebhookParser {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public parseFedExWebhook(payload: any): NormalizedTrackingEvent {
    const raw = payload?.notification?.events?.[0];
    const rawStatus = raw?.eventType || 'UNKNOWN';

    return {
      trackingNumber: payload?.trackingNumber || raw?.trackingNumber,
      carrier: CarrierCode.FEDEX,
      status: this.mapFedExStatus(rawStatus),
      milestoneDescription: raw?.eventDescription || 'FedEx tracking milestone update',
      locationCity: raw?.scanLocation?.city,
      locationState: raw?.scanLocation?.stateOrProvinceCode,
      locationCountry: raw?.scanLocation?.countryCode,
      carrierStatusCode: rawStatus,
      eventTimestamp: new Date(raw?.timestamp || Date.now())
    };
  }

  public parseUpsWebhook(payload: any): NormalizedTrackingEvent {
    const raw = payload?.TrackResponse?.Shipment?.Package?.Activity?.[0];
    const rawStatus = raw?.Status?.Type || 'UNKNOWN';

    return {
      trackingNumber: payload?.TrackResponse?.Shipment?.Package?.TrackingNumber,
      carrier: CarrierCode.UPS,
      status: this.mapUpsStatus(rawStatus),
      milestoneDescription: raw?.Status?.Description || 'UPS tracking milestone update',
      locationCity: raw?.ActivityLocation?.Address?.City,
      locationState: raw?.ActivityLocation?.Address?.StateProvinceCode,
      locationCountry: raw?.ActivityLocation?.Address?.CountryCode,
      carrierStatusCode: rawStatus,
      eventTimestamp: new Date()
    };
  }

  private mapFedExStatus(code: string): FulfillmentStatus {
    switch (code) {
      case 'PU': return FulfillmentStatus.READY_FOR_PICKUP;
      case 'DP': return FulfillmentStatus.SHIPPED;
      case 'IT': return FulfillmentStatus.IN_TRANSIT;
      case 'OD': return FulfillmentStatus.OUT_FOR_DELIVERY;
      case 'DL': return FulfillmentStatus.DELIVERED;
      case 'DE': return FulfillmentStatus.FAILED_ATTEMPT;
      case 'RS': return FulfillmentStatus.RETURNED_TO_SENDER;
      default: return FulfillmentStatus.IN_TRANSIT;
    }
  }

  private mapUpsStatus(code: string): FulfillmentStatus {
    switch (code) {
      case 'M': return FulfillmentStatus.LABEL_GENERATED;
      case 'P': return FulfillmentStatus.READY_FOR_PICKUP;
      case 'I': return FulfillmentStatus.IN_TRANSIT;
      case 'O': return FulfillmentStatus.OUT_FOR_DELIVERY;
      case 'D': return FulfillmentStatus.DELIVERED;
      case 'X': return FulfillmentStatus.FAILED_ATTEMPT;
      default: return FulfillmentStatus.IN_TRANSIT;
    }
  }
}
""")

    print("Fulfillment domain expanded.")

if __name__ == "__main__":
    build_fulfillment_domain()
