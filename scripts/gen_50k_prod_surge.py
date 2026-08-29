import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_surge():
    print("Generating Production Surge Code...")

    # 1. SDK Python Advanced Query Builders
    write_file("sdks/python/novacommerce/query_builder.py", """from typing import Dict, Any, List, Optional
from urllib.parse import urlencode

class ApiQueryBuilder:
    def __init__(self):
        self._params: Dict[str, Any] = {}

    def page(self, page_number: int) -> 'ApiQueryBuilder':
        self._params['page'] = max(1, page_number)
        return self

    def limit(self, limit_count: int) -> 'ApiQueryBuilder':
        self._params['limit'] = min(100, max(1, limit_count))
        return self

    def sort_by(self, field: str, direction: str = 'asc') -> 'ApiQueryBuilder':
        self._params['sortBy'] = field
        self._params['sortOrder'] = 'asc' if direction.lower() == 'asc' else 'desc'
        return self

    def filter(self, field: str, value: Any) -> 'ApiQueryBuilder':
        if value is not None:
            self._params[field] = value
        return self

    def filter_in(self, field: str, values: List[Any]) -> 'ApiQueryBuilder':
        if values:
            self._params[field] = ','.join(str(v) for v in values)
        return self

    def build(self) -> Dict[str, Any]:
        return {k: v for k, v in self._params.items() if v is not None}

    def to_query_string(self) -> str:
        params = self.build()
        return f"?{urlencode(params)}" if params else ""
""")

    # 2. TypeScript SDK Advanced Interceptors
    write_file("sdks/typescript/src/interceptors/retry.interceptor.ts", """export interface RetryConfig {
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
""")

    # 3. Gateway Security Headers
    write_file("services/api-gateway/src/middleware/security-headers.middleware.ts", """import { Request, Response, NextFunction } from 'express';

export function securityHeadersMiddleware() {
  return (req: Request, res: Response, next: NextFunction) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-XSS-Protection', '1; mode=block');
    res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload');
    res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
    res.setHeader('Content-Security-Policy', "default-src 'self'; script-src 'self'; object-src 'none';");
    res.removeHeader('X-Powered-By');
    next();
  };
}
""")

    # 4. Gateway Response Compression
    write_file("services/api-gateway/src/middleware/response-compressor.middleware.ts", """import { Request, Response, NextFunction } from 'express';

export function responseCompressorMiddleware() {
  return (req: Request, res: Response, next: NextFunction) => {
    const acceptEncoding = req.headers['accept-encoding'] || '';
    if (typeof acceptEncoding === 'string' && acceptEncoding.includes('gzip')) {
      res.setHeader('Vary', 'Accept-Encoding');
    }
    next();
  };
}
""")

    print("Production surge generation complete.")

if __name__ == "__main__":
    generate_prod_surge()
