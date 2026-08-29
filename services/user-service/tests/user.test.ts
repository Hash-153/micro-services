import request from 'supertest';
import { createUserApp } from '../src/app.js';
import jwt from 'jsonwebtoken';

describe('User Service Suite', () => {
  const app = createUserApp();
  const secret = process.env.JWT_SECRET || 'super_secret_local_jwt_signing_key_min_32_characters_long';
  const token = jwt.sign({ sub: 'user-001', email: 'test@novacommerce.io', role: 'CUSTOMER' }, secret);

  it('should get and update profile for authenticated user', async () => {
    const getRes = await request(app)
      .get('/api/v1/users/profile')
      .set('Authorization', `Bearer ${token}`);

    expect(getRes.status).toBe(200);
    expect(getRes.body.data.userId).toBe('user-001');

    const putRes = await request(app)
      .put('/api/v1/users/profile')
      .set('Authorization', `Bearer ${token}`)
      .send({ firstName: 'Alexander', lastName: 'Hamilton' });

    expect(putRes.status).toBe(200);
    expect(putRes.body.data.firstName).toBe('Alexander');
  });
});
