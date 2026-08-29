import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface FulfillmentLabelGeneratedEventPayload {
  shipmentId: string; orderId: string; carrier: string; trackingNumber: string; labelUrl: string;
}

export type FulfillmentLabelGeneratedEvent = DomainEvent<FulfillmentLabelGeneratedEventPayload>;

export class FulfillmentLabelGeneratedEventFactory {
  public static create(
    aggregateId: string,
    payload: FulfillmentLabelGeneratedEventPayload,
    producer: string,
    correlationId?: string
  ): FulfillmentLabelGeneratedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'fulfillment.label_generated' as EventType,
      aggregateId,
      aggregateType: 'Shipment',
      version: 1,
      timestamp: new Date().toISOString(),
      correlationId: correlationId || crypto.randomUUID(),
      producer,
      payload
    };
  }
}
