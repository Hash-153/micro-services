import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_colossus():
    print("Generating comprehensive Production Colossus Modules...")

    # 1. SDK Python Advanced Error Handler
    write_file("sdks/python/novacommerce/error_handler.py", """import httpx
from typing import Dict, Any, Optional
from .exceptions import NovaCommerceException, AuthenticationError, NotFoundError, ValidationError, InsufficientStockError, SagaExecutionError

class ApiErrorHandler:
    @staticmethod
    def parse_and_raise(response: httpx.Response) -> None:
        try:
            body = response.json()
            err = body.get('error', {})
            msg = err.get('message', response.text)
            code = err.get('code', 'ERR_UNKNOWN')
            details = err.get('details')
        except Exception:
            msg = response.text
            code = 'ERR_HTTP'
            details = None

        status = response.status_code
        if status == 401:
            raise AuthenticationError(msg)
        elif status == 404:
            raise NotFoundError('Resource', response.url.path)
        elif status == 400:
            raise ValidationError(msg, details)
        elif status == 409 and code == 'ERR_INSUFFICIENT_STOCK':
            raise InsufficientStockError('SKU', 0, 0)
        else:
            raise NovaCommerceException(msg, status_code=status, error_code=code, details=details)
""")

    # 2. TypeScript SDK Query String Serializer
    write_file("sdks/typescript/src/utils/QuerySerializer.ts", """export class QuerySerializer {
  public static serialize(params: Record<string, any>): string {
    const searchParams = new URLSearchParams();

    for (const [key, value] of Object.entries(params)) {
      if (value === undefined || value === null || value === '') {
        continue;
      }
      if (Array.isArray(value)) {
        searchParams.append(key, value.join(','));
      } else if (typeof value === 'object' && !(value instanceof Date)) {
        searchParams.append(key, JSON.stringify(value));
      } else if (value instanceof Date) {
        searchParams.append(key, value.toISOString());
      } else {
        searchParams.append(key, String(value));
      }
    }

    const qs = searchParams.toString();
    return qs ? `?${qs}` : '';
  }
}
""")

    print("Production colossus modules generated.")

if __name__ == "__main__":
    generate_prod_colossus()
