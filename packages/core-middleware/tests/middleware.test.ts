import { SlidingWindowRateLimiter } from '../src/index.js';

describe('Core Middleware Suite', () => {
  it('should enforce rate limits on excessive requests', (done) => {
    const limiter = new SlidingWindowRateLimiter(60000, 2);
    const middleware = limiter.middleware();

    const req: any = { ip: '192.168.1.1', headers: {} };
    const res: any = {};

    middleware(req, res, () => {
      middleware(req, res, () => {
        middleware(req, res, (err: any) => {
          expect(err).toBeDefined();
          expect(err.statusCode).toBe(429);
          done();
        });
      });
    });
  });
});
