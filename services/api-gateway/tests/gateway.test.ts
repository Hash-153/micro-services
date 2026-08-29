import request from 'supertest';
import { createGatewayApp } from '../src/app.js';

describe('API Gateway Suite', () => {
  const app = createGatewayApp();

  it('should return UP on /health', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('UP');
    expect(res.body.service).toBe('api-gateway');
  });

  it('should list configured routes on /routes', async () => {
    const res = await request(app).get('/routes');
    expect(res.status).toBe(200);
    expect(res.body.routes.length).toBeGreaterThan(5);
  });
});
