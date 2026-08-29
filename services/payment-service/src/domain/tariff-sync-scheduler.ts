import { Logger } from '@novacommerce/core-logger';

export class TariffSyncScheduler {
  private logger: Logger;
  private intervalMinutes: number;

  constructor(logger: Logger, intervalMinutes: number = 1440) { // 24-hour sync
    this.logger = logger;
    this.intervalMinutes = intervalMinutes;
  }

  public scheduleDailySync(): void {
    this.logger.info(`Scheduled daily UNSPSC / HS tariff database synchronization (interval: ${this.intervalMinutes}m)`);
  }
}
