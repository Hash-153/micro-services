import { ILogger } from '@novacommerce/core-logger';
import { randomUUID, createHash } from 'crypto';

export interface UserSession {
  sessionId: string;
  userId: string;
  email: string;
  ipAddress: string;
  userAgent: string;
  refreshTokenHash: string;
  isRevoked: boolean;
  expiresAt: Date;
  createdAt: Date;
  lastActivityAt: Date;
}

export class SessionService {
  private readonly sessions: Map<string, UserSession> = new Map();
  private readonly logger: ILogger;

  constructor(logger: ILogger) {
    this.logger = logger.child({ component: 'SessionService' });
  }

  public async createSession(
    userId: string,
    email: string,
    refreshToken: string,
    ipAddress: string = '127.0.0.1',
    userAgent: string = 'Unknown',
    ttlDays: number = 7
  ): Promise<UserSession> {
    const sessionId = randomUUID();
    const refreshTokenHash = createHash('sha256').update(refreshToken).digest('hex');
    const expiresAt = new Date(Date.now() + ttlDays * 24 * 60 * 60 * 1000);

    const session: UserSession = {
      sessionId,
      userId,
      email,
      ipAddress,
      userAgent,
      refreshTokenHash,
      isRevoked: false,
      expiresAt,
      createdAt: new Date(),
      lastActivityAt: new Date()
    };

    this.sessions.set(sessionId, session);
    this.logger.info(`Session created: ${sessionId} for user ${userId}`);
    return session;
  }

  public async getActiveSession(sessionId: string): Promise<UserSession | null> {
    const session = this.sessions.get(sessionId);
    if (!session || session.isRevoked || session.expiresAt < new Date()) {
      return null;
    }
    session.lastActivityAt = new Date();
    return session;
  }

  public async revokeSession(sessionId: string): Promise<boolean> {
    const session = this.sessions.get(sessionId);
    if (session) {
      session.isRevoked = true;
      this.logger.info(`Session revoked: ${sessionId}`);
      return true;
    }
    return false;
  }

  public async revokeAllUserSessions(userId: string): Promise<number> {
    let count = 0;
    for (const session of this.sessions.values()) {
      if (session.userId === userId && !session.isRevoked) {
        session.isRevoked = true;
        count++;
      }
    }
    this.logger.info(`Revoked ${count} sessions for user ${userId}`);
    return count;
  }
}
