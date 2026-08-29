import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_nexus_scale():
    print("Generating comprehensive Production Nexus Scale Modules...")

    # 1. API Gateway Trace ID Header Injector
    write_file("services/api-gateway/src/middleware/trace-id-injector.ts", """import { Request, Response, NextFunction } from 'express';
import { W3cTraceContextPropagator } from '@novacommerce/core-logger';

export class TraceIdInjector {
  public static middleware() {
    return (req: Request, res: Response, next: NextFunction) => {
      const incoming = req.headers['traceparent'] as string | undefined;
      const parsed = W3cTraceContextPropagator.parse(incoming) || W3cTraceContextPropagator.generate();

      const traceparentHeader = W3cTraceContextPropagator.format(parsed);
      res.setHeader('traceparent', traceparentHeader);
      res.setHeader('X-Trace-Id', parsed.traceId);

      (req as any).traceContext = parsed;
      next();
    };
  }
}
""")

    # 2. Notification Template Variable Validator
    write_file("services/notification-service/src/domain/template-variable-validator.ts", """export class TemplateVariableValidator {
  public static extractRequiredVariables(templateHtml: string): string[] {
    const regex = /{{\\s*([a-zA-Z0-9_]+)\\s*}}/g;
    const matches = new Set<string>();
    let m;
    while ((m = regex.exec(templateHtml)) !== null) {
      matches.add(m[1]);
    }
    return Array.from(matches);
  }

  public static validateVariablesSupplied(
    templateHtml: string,
    suppliedVariables: Record<string, any>
  ): { isValid: boolean; missingVariables: string[] } {
    const required = this.extractRequiredVariables(templateHtml);
    const missing: string[] = [];

    for (const v of required) {
      if (suppliedVariables[v] === undefined || suppliedVariables[v] === null) {
        missing.push(v);
      }
    }

    return {
      isValid: missing.length === 0,
      missingVariables: missing
    };
  }
}
""")

    print("Production nexus scale modules generated.")

if __name__ == "__main__":
    generate_prod_nexus_scale()
