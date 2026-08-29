export class LeakyBucketLimiter {
  private capacity: number;
  private leakRatePerSecond: number;
  private waterLevel: number = 0;
  private lastLeakTimestamp: number = Date.now();

  constructor(capacity: number = 100, leakRatePerSecond: number = 10) {
    this.capacity = capacity;
    this.leakRatePerSecond = leakRatePerSecond;
  }

  public allowRequest(cost: number = 1): boolean {
    this.leak();
    if (this.waterLevel + cost <= this.capacity) {
      this.waterLevel += cost;
      return true;
    }
    return false;
  }

  private leak(): void {
    const now = Date.now();
    const elapsedSeconds = (now - this.lastLeakTimestamp) / 1000;
    const leaked = elapsedSeconds * this.leakRatePerSecond;

    if (leaked > 0) {
      this.waterLevel = Math.max(0, this.waterLevel - leaked);
      this.lastLeakTimestamp = now;
    }
  }
}
