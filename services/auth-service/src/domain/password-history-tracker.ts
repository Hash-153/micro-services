export class PasswordHistoryTracker {
  private static readonly MAX_HISTORY_LENGTH = 5;

  public static isPasswordReused(newPasswordHash: string, historicalHashes: string[]): boolean {
    const recentHashes = historicalHashes.slice(-this.MAX_HISTORY_LENGTH);
    return recentHashes.includes(newPasswordHash);
  }

  public static appendHistory(newPasswordHash: string, historicalHashes: string[]): string[] {
    const updated = [...historicalHashes, newPasswordHash];
    if (updated.length > this.MAX_HISTORY_LENGTH) {
      return updated.slice(-this.MAX_HISTORY_LENGTH);
    }
    return updated;
  }
}
