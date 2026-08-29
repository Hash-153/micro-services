import { CarrierCode } from '@novacommerce/core-types';

export interface CarrierSlaPromise {
  carrier: CarrierCode;
  serviceLevel: string;
  orderPlacedAt: Date;
  warehouseCutoffTimeLocal: string; // e.g. "16:00"
  estimatedShipDate: Date;
  estimatedDeliveryDate: Date;
  guaranteedByDate?: Date;
  isCutoffExceeded: boolean;
}

export class CarrierSlaCalculator {
  public static calculateDeliveryCommitment(
    orderPlacedAt: Date,
    carrier: CarrierCode,
    serviceLevel: string,
    transitDays: number = 3
  ): CarrierSlaPromise {
    const cutoffHour = 16; // 4:00 PM local cutoff
    const orderHour = orderPlacedAt.getHours();
    const isCutoffExceeded = orderHour >= cutoffHour;

    const shipDate = new Date(orderPlacedAt);
    if (isCutoffExceeded) {
      shipDate.setDate(shipDate.getDate() + 1);
    }
    // Skip weekend for dispatch
    if (shipDate.getDay() === 6) shipDate.setDate(shipDate.getDate() + 2); // Saturday -> Monday
    if (shipDate.getDay() === 0) shipDate.setDate(shipDate.getDate() + 1); // Sunday -> Monday

    const deliveryDate = new Date(shipDate);
    let addedDays = 0;
    while (addedDays < transitDays) {
      deliveryDate.setDate(deliveryDate.getDate() + 1);
      if (deliveryDate.getDay() !== 0 && deliveryDate.getDay() !== 6) {
        addedDays++;
      }
    }

    return {
      carrier,
      serviceLevel,
      orderPlacedAt,
      warehouseCutoffTimeLocal: '16:00',
      estimatedShipDate: shipDate,
      estimatedDeliveryDate: deliveryDate,
      guaranteedByDate: serviceLevel.includes('EXPRESS') ? deliveryDate : undefined,
      isCutoffExceeded
    };
  }
}
