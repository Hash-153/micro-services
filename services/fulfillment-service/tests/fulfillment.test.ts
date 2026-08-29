import request from 'supertest';
import { createFulfillmentApp } from '../src/app.js';

describe('Fulfillment Service Suite', () => {
  const app = createFulfillmentApp();

  it('should generate shipment and tracking number', async () => {
    const res = await request(app)
      .post('/api/v1/fulfillment/shipments')
      .send({ orderId: 'ord-888' });

    expect(res.status).toBe(201);
    expect(res.body.data.trackingNumber).toBeDefined();
    expect(res.body.data.status).toBe('LABEL_GENERATED');
  });
});
