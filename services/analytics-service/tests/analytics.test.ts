import request from 'supertest';
import { createAnalyticsApp } from '../src/app.js';

describe('Analytics Service Suite', () => {
  const app = createAnalyticsApp();

  it('should track analytics events and provide summary', async () => {
    await request(app)
      .post('/api/v1/analytics/events')
      .send({ eventName: 'product_viewed', properties: { sku: 'SKU-001' } });

    const res = await request(app).get('/api/v1/analytics/summary');
    expect(res.status).toBe(200);
    expect(res.body.data.totalEvents).toBeGreaterThan(0);
    expect(res.body.data.countsByEvent['product_viewed']).toBe(1);
  });
});
