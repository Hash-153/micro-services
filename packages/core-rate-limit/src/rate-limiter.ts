export interface RateLimitConfig {
  requests: number;
  windowMs: number;
  skipSuccessfulRequests?: boolean;
  skipFailedRequests?: boolean;
}

export interface RateLimitResult {
  allowed: boolean;
  limit: number;
  remaining: number;
  reset: number;
  retryAfter?: number;
}

export class RateLimiter {
  private windows: Map<string, {
    count: number;
    resetAt: number;
  }> = new Map();
  private config: RateLimitConfig;

  constructor(config: RateLimitConfig) {
    this.config = {
      requests: config.requests,
      windowMs: config.windowMs,
      skipSuccessfulRequests: config.skipSuccessfulRequests || false,
      skipFailedRequests: config.skipFailedRequests || false
    };
  }

  public async check(key: string, success?: boolean): Promise<RateLimitResult> {
    const now = Date.now();
    const window = this.windows.get(key);

    // Create new window if doesn't exist or expired
    if (!window || now >= window.resetAt) {
      const newWindow = {
        count: 1,
        resetAt: now + this.config.windowMs
      };
      this.windows.set(key, newWindow);

      return {
        allowed: true,
        limit: this.config.requests,
        remaining: this.config.requests - 1,
        reset: newWindow.resetAt
      };
    }

    // Check if should skip based on success/failure
    if (success === true && this.config.skipSuccessfulRequests) {
      return {
        allowed: true,
        limit: this.config.requests,
        remaining: this.config.requests - window.count,
        reset: window.resetAt
      };
    }

    if (success === false && this.config.skipFailedRequests) {
      return {
        allowed: true,
        limit: this.config.requests,
        remaining: this.config.requests - window.count,
        reset: window.resetAt
      };
    }

    // Check if limit exceeded
    if (window.count >= this.config.requests) {
      const retryAfter = Math.ceil((window.resetAt - now) / 1000);
      
      return {
        allowed: false,
        limit: this.config.requests,
        remaining: 0,
        reset: window.resetAt,
        retryAfter
      };
    }

    // Increment counter
    window.count++;
    this.windows.set(key, window);

    return {
      allowed: true,
      limit: this.config.requests,
      remaining: this.config.requests - window.count,
      reset: window.resetAt
    };
  }

  public async reset(key: string): Promise<void> {
    this.windows.delete(key);
  }

  public async resetAll(): Promise<void> {
    this.windows.clear();
  }

  public async getWindow(key: string): Promise<{ count: number; resetAt: number } | null> {
    const window = this.windows.get(key);
    if (!window || Date.now() >= window.resetAt) {
      return null;
    }
    return window;
  }

  public async cleanup(): Promise<void> {
    const now = Date.now();
    for (const [key, window] of this.windows.entries()) {
      if (now >= window.resetAt) {
        this.windows.delete(key);
      }
    }
  }
}
