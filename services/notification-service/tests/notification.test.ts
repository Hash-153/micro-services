import request from 'supertest';
import { createNotificationApp } from '../src/app.js';

describe('Notification Service Suite', () => {
  const app = createNotificationApp();

  it('should accept and dispatch notification payload', async () => {
    const res = await request(app)
      .post('/api/v1/notifications/send')
      .send({
        recipient: 'customer@example.com',
        channel: 'EMAIL',
        template: 'order_confirmation',
        data: { orderNumber: 'ORD-123' }
      });

    expect(res.status).toBe(202);
    expect(res.body.data.status).toBe('DELIVERED');
  });
});
