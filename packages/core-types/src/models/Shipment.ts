import { FulfillmentStatus, CarrierCode } from '../enums/FulfillmentStatus.js';
import { AddressEntity } from './User.js';

export interface ShipmentEntity {
  id: string;
  shipmentNumber: string;
  orderId: string;
  status: FulfillmentStatus;
  carrier: CarrierCode;
  serviceLevel: string; // e.g. 'STANDARD_GROUND', 'EXPRESS_2_DAY', 'OVERNIGHT'
  trackingNumber?: string;
  trackingUrl?: string;
  shippingLabelUrl?: string;
  originWarehouseId: string;
  destinationAddress: AddressEntity;
  weightGrams: number;
  dimensionsMm: {
    length: number;
    width: number;
    height: number;
  };
  dispatchedAt?: Date;
  deliveredAt?: Date;
  createdAt: Date;
  updatedAt: Date;
}
