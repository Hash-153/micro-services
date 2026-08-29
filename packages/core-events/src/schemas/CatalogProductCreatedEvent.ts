import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface CatalogProductCreatedEventPayload {
  productId: string; sku: string; name: string; categoryId: string; basePriceCents: number; currency: string;
}

export type CatalogProductCreatedEvent = DomainEvent<CatalogProductCreatedEventPayload>;

export class CatalogProductCreatedEventFactory {
  public static create(
    aggregateId: string,
    payload: CatalogProductCreatedEventPayload,
    producer: string,
    correlationId?: string
  ): CatalogProductCreatedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'catalog.product.created' as EventType,
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
