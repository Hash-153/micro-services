import { InMemoryEventBus, DomainEventFactory } from '../src/index.js';
import { EventType } from '@novacommerce/core-types';

describe('Core Events Suite', () => {
  let eventBus: InMemoryEventBus;

  beforeEach(async () => {
    eventBus = new InMemoryEventBus();
    await eventBus.connect();
  });

  afterEach(async () => {
    await eventBus.disconnect();
  });

  it('should publish and receive subscribed events correctly', async () => {
    let receivedPayload: any = null;

    await eventBus.subscribe(EventType.ORDER_CREATED, async (event) => {
      receivedPayload = event.payload;
    });

    const domainEvent = DomainEventFactory.create(
      EventType.ORDER_CREATED,
      'order_123',
      'Order',
      { orderNumber: 'ORD-2026-001', total: 9900 },
      'order-service'
    );

    await eventBus.publish(domainEvent);

    expect(receivedPayload).toEqual({ orderNumber: 'ORD-2026-001', total: 9900 });
  });
});
