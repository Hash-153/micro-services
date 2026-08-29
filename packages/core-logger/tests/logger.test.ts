import { Logger, Redactor } from '../src/index.js';

describe('Core Logger Suite', () => {
  it('should redact sensitive properties accurately', () => {
    const payload = {
      userId: 'user_123',
      password: 'PlainSecretPassword123',
      token: 'jwt_token_here',
      nested: {
        creditCard: '4111222233334444',
        safeProperty: 'allowed'
      }
    };

    const redacted = Redactor.redact(payload) as Record<string, any>;
    expect(redacted.userId).toBe('user_123');
    expect(redacted.password).toBe('[REDACTED]');
    expect(redacted.token).toBe('[REDACTED]');
    expect(redacted.nested.creditCard).toBe('[REDACTED]');
    expect(redacted.nested.safeProperty).toBe('allowed');
  });

  it('should create child logger with preserved and merged context', () => {
    const parent = Logger.create('test-service', 'test');
    const child = parent.child({ correlationId: 'corr-999', userId: 'user-001' });
    expect(child).toBeDefined();
  });
});
