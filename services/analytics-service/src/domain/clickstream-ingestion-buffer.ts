import { ClickstreamEventPayload } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export class ClickstreamIngestionBuffer {
  private logger: Logger;
  private buffer: ClickstreamEventPayload[] = [];
  private readonly maxBufferSize: number;
  private readonly flushIntervalMs: number;

  constructor(logger: Logger, maxBufferSize: number = 1000, flushIntervalMs: number = 5000) {
    this.logger = logger;
    this.maxBufferSize = maxBufferSize;
    this.flushIntervalMs = flushIntervalMs;
  }

  public enqueue(event: ClickstreamEventPayload): void {
    this.buffer.push(event);
    if (this.buffer.length >= this.maxBufferSize) {
      this.flush();
    }
  }

  public flush(): ClickstreamEventPayload[] {
    if (this.buffer.length === 0) return [];
    const batch = [...this.buffer];
    this.buffer = [];
    this.logger.info(`Flushed ${batch.length} clickstream telemetry events to analytics warehouse`);
    return batch;
  }

  public get pendingCount(): number {
    return this.buffer.length;
  }
}
