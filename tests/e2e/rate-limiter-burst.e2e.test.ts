import { SlidingWindowRateLimiter } from '@novacommerce/core-middleware';

describe('E2E Scenario: API Gateway DoS Protection & Sliding Window Rate Limiting', () => {
  it('should permit requests within rate limit and reject bursts', (done) => {
    const limiter = new SlidingWindowRateLimiter(60000, 3);
    const middleware = limiter.middleware();
    const req: any = { ip: '10.0.0.99', headers: {} };
    const res: any = {};

    let successCount = 0;
    const runNext = (i: number) => {
      middleware(req, res, (err: any) => {
        if (!err) {
          successCount++;
          if (i < 3) runNext(i + 1);
        } else {
          expect(err.statusCode).toBe(429);
          expect(successCount).toBe(3);
          done();
        }
      });
    };

    runNext(1);
  });
});
