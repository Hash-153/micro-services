import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v9():
    print("Generating comprehensive Production V9 Modules...")

    # 1. User Service Password History & Enforcer
    write_file("services/auth-service/src/domain/password-history-tracker.ts", """export class PasswordHistoryTracker {
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
""")

    # 2. Notification Service Rate Limiter
    write_file("services/notification-service/src/domain/notification-rate-limiter.ts", """export class NotificationRateLimiter {
  private recipientHistory: Map<string, number[]> = new Map();
  private readonly maxPerHour: number;

  constructor(maxPerHour: number = 20) {
    this.maxPerHour = maxPerHour;
  }

  public isRateLimited(recipient: string): boolean {
    const now = Date.now();
    const oneHourAgo = now - 3600000;
    const history = (this.recipientHistory.get(recipient) || []).filter(ts => ts > oneHourAgo);

    if (history.length >= this.maxPerHour) {
      return true;
    }

    history.push(now);
    this.recipientHistory.set(recipient, history);
    return false;
  }
}
""")

    print("Production V9 modules generated.")

if __name__ == "__main__":
    generate_prod_v9()
