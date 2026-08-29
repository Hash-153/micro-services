export class NotificationRateLimiter {
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
