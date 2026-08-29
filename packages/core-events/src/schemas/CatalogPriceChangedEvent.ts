import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface CatalogPriceChangedEventPayload {
  productId: string; sku: string; oldPriceCents: number; newPriceCents: number; currency: string;
}

export type CatalogPriceChangedEvent = DomainEvent<CatalogPriceChangedEventPayload>;

export class CatalogPriceChangedEventFactory {
  public static create(
    aggregateId: string,
    payload: CatalogPriceChangedEventPayload,
    producer: string,
    correlationId?: string
  ): CatalogPriceChangedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'catalog.price.changed' as EventType,
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
