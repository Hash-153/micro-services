import { CarrierCode, FulfillmentStatus } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export interface TrackingPollResult {
  trackingNumber: string;
  carrier: CarrierCode;
  latestStatus: FulfillmentStatus;
  estimatedDeliveryDate?: Date;
  actualDeliveryDate?: Date;
  statusDescription: string;
  isTerminalStatus: boolean;
}

export class CarrierTrackingPoller {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async pollCarrierApi(trackingNumber: string, carrier: CarrierCode): Promise<TrackingPollResult> {
    this.logger.info(`Polling ${carrier} tracking status for #${trackingNumber}`);

    // In production, queries FedEx Track API / UPS Track API / USPS Web Tools
    const isDelivered = trackingNumber.endsWith('9');
    const isOutForDelivery = trackingNumber.endsWith('7');

    let latestStatus = FulfillmentStatus.IN_TRANSIT;
    let isTerminal = false;

    if (isDelivered) {
      latestStatus = FulfillmentStatus.DELIVERED;
      isTerminal = true;
    } else if (isOutForDelivery) {
      latestStatus = FulfillmentStatus.OUT_FOR_DELIVERY;
    }

    return {
      trackingNumber,
      carrier,
      latestStatus,
      estimatedDeliveryDate: isDelivered ? undefined : new Date(Date.now() + 86400000),
      actualDeliveryDate: isDelivered ? new Date() : undefined,
      statusDescription: `Package status: ${latestStatus}`,
      isTerminalStatus: isTerminal
    };
  }
}
