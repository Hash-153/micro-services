import request from 'supertest';
import { createAuthApp } from '../src/app.js';
import { InMemoryUserAuthRepository } from '../src/repositories/user-auth.repository.js';

describe('Auth Service Suite', () => {
  let app: any;

  beforeEach(() => {
    app = createAuthApp(new InMemoryUserAuthRepository());
  });

  it('should register a new user and return JWT tokens', async () => {
    const res = await request(app)
      .post('/api/v1/auth/register')
      .send({
        email: 'developer@novacommerce.io',
        password: 'Password123!',
        firstName: 'John',
        lastName: 'Engineer'
      });

    expect(res.status).toBe(201);
    expect(res.body.success).toBe(true);
    expect(res.body.data.accessToken).toBeDefined();
    expect(res.body.data.user.email).toBe('developer@novacommerce.io');
  });

  it('should login an existing registered user', async () => {
    await request(app)
      .post('/api/v1/auth/register')
      .send({
        email: 'developer@novacommerce.io',
        password: 'Password123!',
        firstName: 'John',
        lastName: 'Engineer'
      });

    const loginRes = await request(app)
      .post('/api/v1/auth/login')
      .send({
        email: 'developer@novacommerce.io',
        password: 'Password123!'
      });

    expect(loginRes.status).toBe(200);
    expect(loginRes.body.data.accessToken).toBeDefined();
  });
});
