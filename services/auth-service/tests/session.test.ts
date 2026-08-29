import { SessionService } from '../src/services/session.service.js';
import { Logger } from '@novacommerce/core-logger';

describe('Auth Session Service Suite', () => {
  const logger = Logger.create('test');
  const service = new SessionService(logger);

  it('should create and retrieve active session', async () => {
    const session = await service.createSession('usr-100', 'usr@test.io', 'tok_refresh_123');
    expect(session.sessionId).toBeDefined();
    expect(session.isRevoked).toBe(false);

    const active = await service.getActiveSession(session.sessionId);
    expect(active).toBeDefined();
    expect(active?.userId).toBe('usr-100');
  });

  it('should revoke session on logout', async () => {
    const session = await service.createSession('usr-200', 'usr2@test.io', 'tok_refresh_456');
    await service.revokeSession(session.sessionId);
    const active = await service.getActiveSession(session.sessionId);
    expect(active).toBeNull();
  });
});
