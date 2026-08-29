import request from 'supertest';
import { createOrderApp } from '../src/app.js';
import { randomUUID } from 'crypto';

describe('Order Service Suite', () => {
  const app = createOrderApp();

  it('should create order and compute tax automatically', async () => {
    const res = await request(app)
      .post('/api/v1/orders')
      .send({
        shippingAddressId: randomUUID(),
        billingAddressId: randomUUID(),
        items: [{ sku: 'SKU-001', quantity: 2 }],
        idempotencyKey: randomUUID()
      });

    expect(res.status).toBe(201);
    expect(res.body.data.orderNumber).toBeDefined();
    expect(res.body.data.subtotalAmount.amount).toBe(5998);
    expect(res.body.data.taxAmount.amount).toBeGreaterThan(0);
  });
});
