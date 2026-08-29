export class SessionInvalidationManager {
  private blacklistedTokens: Map<string, number> = new Map(); // tokenHash -> expiresAt

  public blacklistToken(tokenHash: string, expiresAt: number): void {
    this.blacklistedTokens.set(tokenHash, expiresAt);
  }

  public isTokenBlacklisted(tokenHash: string): boolean {
    const expiresAt = this.blacklistedTokens.get(tokenHash);
    if (!expiresAt) return false;

    if (Date.now() > expiresAt) {
      this.blacklistedTokens.delete(tokenHash);
      return false;
    }

    return true;
  }

  public purgeExpired(): void {
    const now = Date.now();
    for (const [tokenHash, expiresAt] of this.blacklistedTokens.entries()) {
      if (now > expiresAt) {
        this.blacklistedTokens.delete(tokenHash);
      }
    }
  }
}
