import { IEventBus, OutboxRepository } from './interfaces.js';
import { ILogger } from '@novacommerce/core-logger';

export class OutboxProcessor {
  private readonly repo: OutboxRepository;
  private readonly eventBus: IEventBus;
  private readonly logger: ILogger;
  private isRunning: boolean = false;
  private pollIntervalMs: number;
  private timerHandle?: NodeJS.Timeout;

  constructor(repo: OutboxRepository, eventBus: IEventBus, logger: ILogger, pollIntervalMs: number = 1000) {
    this.repo = repo;
    this.eventBus = eventBus;
    this.logger = logger.child({ component: 'OutboxProcessor' });
    this.pollIntervalMs = pollIntervalMs;
  }

  public start(): void {
    if (this.isRunning) return;
    this.isRunning = true;
    this.logger.info('OutboxProcessor started polling loop.');
    this.scheduleNextRun();
  }

  public stop(): void {
    this.isRunning = false;
    if (this.timerHandle) {
      clearTimeout(this.timerHandle);
    }
    this.logger.info('OutboxProcessor stopped.');
  }

  public async processBatch(limit: number = 50): Promise<number> {
    const pendingEvents = await this.repo.fetchPendingEvents(limit);
    if (pendingEvents.length === 0) {
      return 0;
    }

    let processedCount = 0;
    for (const event of pendingEvents) {
      try {
        await this.eventBus.publish(event);
        await this.repo.markEventPublished(event.id);
        processedCount++;
      } catch (err: any) {
        this.logger.error(`Failed to publish outbox event: ${event.id}`, err);
        await this.repo.markEventFailed(event.id, err?.message || 'Unknown publication error');
      }
    }

    return processedCount;
  }

  private scheduleNextRun(): void {
    if (!this.isRunning) return;
    this.timerHandle = setTimeout(async () => {
      try {
        await this.processBatch();
      } catch (err) {
        this.logger.error('Error during outbox batch polling cycle', err);
      } finally {
        this.scheduleNextRun();
      }
    }, this.pollIntervalMs);
  }
}
