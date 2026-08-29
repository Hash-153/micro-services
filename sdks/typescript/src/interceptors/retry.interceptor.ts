export interface RetryConfig {
  maxRetries: number;
  initialDelayMs: number;
  maxDelayMs: number;
  backoffFactor: number;
  retryableStatusCodes: number[];
}

export class RetryInterceptor {
  private config: RetryConfig;

  constructor(config: Partial<RetryConfig> = {}) {
    this.config = {
      maxRetries: config.maxRetries ?? 3,
      initialDelayMs: config.initialDelayMs ?? 100,
      maxDelayMs: config.maxDelayMs ?? 3000,
      backoffFactor: config.backoffFactor ?? 2.0,
      retryableStatusCodes: config.retryableStatusCodes ?? [408, 429, 500, 502, 503, 504]
    };
  }

  public async executeWithRetry<T>(requestFn: () => Promise<T>): Promise<T> {
    let attempt = 0;
    while (true) {
      attempt++;
      try {
        return await requestFn();
      } catch (error: any) {
        const statusCode = error?.statusCode || error?.status;
        const isRetryable = this.config.retryableStatusCodes.includes(statusCode) || error?.name === 'FetchError';

        if (!isRetryable || attempt > this.config.maxRetries) {
          throw error;
        }

        const jitter = Math.floor(Math.random() * 50);
        const delay = Math.min(
          this.config.maxDelayMs,
          this.config.initialDelayMs * Math.pow(this.config.backoffFactor, attempt - 1) + jitter
        );

        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }
}
