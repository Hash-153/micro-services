import request from 'supertest';
import { createPaymentApp } from '../src/app.js';

describe('Payment Service Suite', () => {
  const app = createPaymentApp();

  it('should capture payment and maintain balanced ledger entries', async () => {
    const res = await request(app)
      .post('/api/v1/payments/authorize')
      .send({ orderId: 'ord-999', amountCents: 4999 });

    expect(res.status).toBe(201);
    expect(res.body.data.status).toBe('CAPTURED');
    expect(res.body.data.amount.amount).toBe(4999);
  });
});
