import request from 'supertest';
import { createInventoryApp } from '../src/app.js';

describe('Inventory Service Suite', () => {
  const app = createInventoryApp();

  it('should set stock and reserve successfully', async () => {
    await request(app)
      .post('/api/v1/inventory/stock')
      .send({ sku: 'SKU-PHONE-128', quantity: 50 });

    const res = await request(app)
      .post('/api/v1/inventory/reserve')
      .send({ orderId: 'ord-test-001', sku: 'SKU-PHONE-128', quantity: 2 });

    expect(res.status).toBe(201);
    expect(res.body.data.quantity).toBe(2);
  });

  it('should fail reservation if insufficient stock', async () => {
    const res = await request(app)
      .post('/api/v1/inventory/reserve')
      .send({ orderId: 'ord-test-002', sku: 'SKU-PHONE-128', quantity: 9999 });

    expect(res.status).toBe(400);
    expect(res.body.error.code).toBe('ERR_INVENTORY_INSUFFICIENT_STOCK');
  });
});
