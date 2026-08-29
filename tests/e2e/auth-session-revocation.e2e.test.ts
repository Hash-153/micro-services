import { SessionService } from '../../services/auth-service/src/services/session.service.js';
import { Logger } from '@novacommerce/core-logger';

describe('E2E Scenario: User Session Invalidation & Distributed Token Revocation', () => {
  const logger = Logger.create('test-session-e2e');
  const sessionService = new SessionService(logger);

  it('should create active session and revoke it on user logout', async () => {
    const session = await sessionService.createSession('usr-session-001', '127.0.0.1', 'Mozilla/5.0');
    expect(session.id).toBeDefined();
    expect(session.userId).toBe('usr-session-001');
    expect(session.isRevoked).toBe(false);

    const activeSessions = await sessionService.getUserSessions('usr-session-001');
    expect(activeSessions.length).toBe(1);

    await sessionService.revokeSession(session.id);
    const updatedSessions = await sessionService.getUserSessions('usr-session-001');
    expect(updatedSessions.length).toBe(0);
  });
});
