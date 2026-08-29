import { InMemoryShipmentRepository } from '../repositories/shipment.repository.js';
import { ShipmentEntity, FulfillmentStatus, CarrierCode } from '@novacommerce/core-types';
import { IEventBus, DomainEventFactory } from '@novacommerce/core-events';
import { EventType } from '@novacommerce/core-types';
import { randomUUID } from 'crypto';

export class FulfillmentService {
  private readonly repo: InMemoryShipmentRepository;
  private readonly eventBus?: IEventBus;

  constructor(repo: InMemoryShipmentRepository, eventBus?: IEventBus) {
    this.repo = repo;
    this.eventBus = eventBus;
  }

  public async createShipment(
    orderId: string,
    destinationAddress: any,
    carrier: CarrierCode = CarrierCode.MOCK_CARRIER,
    correlationId?: string
  ): Promise<ShipmentEntity> {
    const trackingNumber = `TRK-${carrier}-${Math.floor(100000000 + Math.random() * 900000000)}`;
    const shipment: ShipmentEntity = {
      id: randomUUID(),
      shipmentNumber: `SHP-${Date.now()}`,
      orderId,
      status: FulfillmentStatus.LABEL_GENERATED,
      carrier,
      serviceLevel: 'STANDARD_GROUND',
      trackingNumber,
      trackingUrl: `https://tracking.novacommerce.io/${trackingNumber}`,
      shippingLabelUrl: `https://cdn.novacommerce.io/labels/${trackingNumber}.pdf`,
      originWarehouseId: 'WH-MAIN-01',
      destinationAddress,
      weightGrams: 1200,
      dimensionsMm: { length: 300, width: 200, height: 100 },
      createdAt: new Date(),
      updatedAt: new Date()
    };

    const saved = await this.repo.create(shipment);

    if (this.eventBus) {
      const event = DomainEventFactory.create(
        EventType.FULFILLMENT_CREATED,
        saved.id,
        'Shipment',
        saved,
        'fulfillment-service',
        correlationId
      );
      await this.eventBus.publish(event);
    }

    return saved;
  }
}
