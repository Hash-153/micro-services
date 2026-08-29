import request from 'supertest';
import { createCatalogApp } from '../src/app.js';
import { Currency } from '@novacommerce/core-types';

describe('Catalog Service Suite', () => {
  const app = createCatalogApp();

  it('should create and fetch product', async () => {
    const createRes = await request(app)
      .post('/api/v1/catalog/products')
      .send({
        sku: 'SKU-LAPTOP-01',
        name: 'Pro Ultrabook 16-inch',
        slug: 'pro-ultrabook-16',
        description: 'High performance engineer laptop',
        categoryId: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
        basePrice: { amount: 199900, currency: Currency.USD },
        tags: ['electronics', 'computers']
      });

    expect(createRes.status).toBe(201);
    const productId = createRes.body.data.id;

    const getRes = await request(app).get(`/api/v1/catalog/products/${productId}`);
    expect(getRes.status).toBe(200);
    expect(getRes.body.data.sku).toBe('SKU-LAPTOP-01');
  });
});
