import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface CatalogProductUpdatedEventPayload {
  productId: string; sku: string; updatedFields: string[];
}

export type CatalogProductUpdatedEvent = DomainEvent<CatalogProductUpdatedEventPayload>;

export class CatalogProductUpdatedEventFactory {
  public static create(
    aggregateId: string,
    payload: CatalogProductUpdatedEventPayload,
    producer: string,
    correlationId?: string
  ): CatalogProductUpdatedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'catalog.product.updated' as EventType,
      aggregateId,
      aggregateType: 'Product',
      version: 1,
      timestamp: new Date().toISOString(),
      correlationId: correlationId || crypto.randomUUID(),
      producer,
      payload
    };
  }
}
