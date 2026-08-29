import { InMemoryShipmentRepository } from '../../services/fulfillment-service/src/repositories/shipment.repository.js';
import { FulfillmentService } from '../../services/fulfillment-service/src/services/fulfillment.service.js';
import { CarrierCode } from '@novacommerce/core-types';

describe('E2E Scenario: Multi-Carrier Shipping Label Generation & Tracking Milestones', () => {
  let fulfillmentService: FulfillmentService;

  beforeEach(() => {
    fulfillmentService = new FulfillmentService(new InMemoryShipmentRepository());
  });

  it('should generate carrier label with valid tracking number and URL', async () => {
    const shipment = await fulfillmentService.createShipment('ord-shp-001', {
      recipientName: 'Alice Walker',
      streetLine1: '500 Tech Blvd',
      city: 'Austin',
      stateOrProvince: 'TX',
      postalCode: '78701',
      countryCode: 'US'
    }, CarrierCode.FEDEX);

    expect(shipment.id).toBeDefined();
    expect(shipment.trackingNumber).toContain('TRK-FEDEX-');
    expect(shipment.trackingUrl).toContain('tracking.novacommerce.io');
    expect(shipment.status).toBe('LABEL_GENERATED');
  });
});
