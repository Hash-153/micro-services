import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def generate_part2():
    print("Generating comprehensive Part 2 enterprise microservices architecture...")

    services = [
        "auth-service", "user-service", "catalog-service", "inventory-service",
        "order-service", "payment-service", "fulfillment-service",
        "notification-service", "analytics-service", "api-gateway"
    ]

    # =========================================================================
    # 1. 30 Microservice Business Logic Service Layer Implementations (v4, v5, v6)
    # =========================================================================
    for svc in services:
        for idx in range(4, 7):
            srv_name = f"{svc.replace('-', '_').title().replace('_', '')}DomainServiceV{idx}"
            ts_code = f"""import {{ Logger }} from '@novacommerce/core-logger';

export interface DomainOperationContextV{idx} {{
  traceId: string;
  userId: string;
  tenantId: string;
  operationName: string;
  initiatedAt: Date;
}}

export interface OperationResultV{idx}<T> {{
  isSuccess: boolean;
  data?: T;
  errorCode?: string;
  errorMessage?: string;
  auditRecordId: string;
}}

export class {srv_name} {{
  private logger: Logger;

  constructor(logger: Logger) {{
    this.logger = logger;
  }}

  public async executePipeline<TInput, TOutput>(
    ctx: DomainOperationContextV{idx},
    input: TInput,
    processor: (ctx: DomainOperationContextV{idx}, input: TInput) => Promise<TOutput>
  ): Promise<OperationResultV{idx}<TOutput>> {{
    this.logger.info(`Starting enterprise pipeline [${{ctx.operationName}}] for tenant ${{ctx.tenantId}} (trace: ${{ctx.traceId}}) in {svc}`);

    try {{
      this.validateContext(ctx);
      const output = await processor(ctx, input);

      const auditId = `aud_${{Date.now()}}_${{Math.random().toString(36).slice(2, 8)}}`;
      this.logger.info(`Pipeline [${{ctx.operationName}}] completed successfully. AuditId: ${{auditId}}`);

      return {{
        isSuccess: true,
        data: output,
        auditRecordId: auditId
      }};
    }} catch (err: any) {{
      this.logger.error(`Pipeline [${{ctx.operationName}}] failed in {svc}:`, err);
      return {{
        isSuccess: false,
        errorCode: 'ERR_DOMAIN_EXECUTION_FAILURE',
        errorMessage: err.message,
        auditRecordId: `aud_err_${{Date.now()}}`
      }};
    }}
  }}

  private validateContext(ctx: DomainOperationContextV{idx}): void {{
    if (!ctx.traceId || !ctx.tenantId || !ctx.operationName) {{
      throw new Error('Invalid DomainOperationContext: traceId, tenantId, and operationName are required');
    }}
  }}
}}
"""
            write_file(f"services/{svc}/src/domain/services/{srv_name.lower()}.ts", ts_code)

    # =========================================================================
    # 2. 30 Microservice Distributed Cache Store Layer Adapters (v4, v5, v6)
    # =========================================================================
    for svc in services:
        for idx in range(4, 7):
            cache_name = f"{svc.replace('-', '_').title().replace('_', '')}CacheStoreV{idx}"
            ts_code = f"""import {{ Logger }} from '@novacommerce/core-logger';

export class {cache_name} {{
  private memoryCache: Map<string, {{ value: any; expiresAt: number }}> = new Map();
  private logger: Logger;
  private defaultTtlMs: number;

  constructor(logger: Logger, defaultTtlMs: number = 300000) {{ // 5 mins
    this.logger = logger;
    this.defaultTtlMs = defaultTtlMs;
  }}

  public async get<T>(key: string): Promise<T | null> {{
    const entry = this.memoryCache.get(key);
    if (!entry) return null;

    if (Date.now() > entry.expiresAt) {{
      this.memoryCache.delete(key);
      this.logger.info(`Cache expired for key [${{key}}] in {svc}`);
      return null;
    }}

    return entry.value as T;
  }}

  public async set<T>(key: string, value: T, ttlMs?: number): Promise<void> {{
    const expiresAt = Date.now() + (ttlMs || this.defaultTtlMs);
    this.memoryCache.set(key, {{ value, expiresAt }});
  }}

  public async del(key: string): Promise<boolean> {{
    return this.memoryCache.delete(key);
  }}

  public async clearPrefix(prefix: string): Promise<number> {{
    let count = 0;
    for (const k of this.memoryCache.keys()) {{
      if (k.startsWith(prefix)) {{
        this.memoryCache.delete(k);
        count++;
      }}
    }}
    return count;
  }}
}}
"""
            write_file(f"services/{svc}/src/infrastructure/cache/{cache_name.lower()}.ts", ts_code)

    # =========================================================================
    # 3. 30 Microservice Metrics & Prometheus Exporter Layer (v4, v5, v6)
    # =========================================================================
    for svc in services:
        for idx in range(4, 7):
            metrics_name = f"{svc.replace('-', '_').title().replace('_', '')}TelemetryExporterV{idx}"
            ts_code = f"""export interface ServiceMetricPointV{idx} {{
  metricName: string;
  serviceName: '{svc}';
  metricType: 'COUNTER' | 'GAUGE' | 'HISTOGRAM';
  value: number;
  tags: Record<string, string>;
  timestamp: Date;
}}

export class {metrics_name} {{
  private points: ServiceMetricPointV{idx}[] = [];

  public recordMetric(metricName: string, value: number, metricType: ServiceMetricPointV{idx}['metricType'] = 'COUNTER', tags: Record<string, string> = {{}}): void {{
    this.points.push({{
      metricName,
      serviceName: '{svc}',
      metricType,
      value,
      tags,
      timestamp: new Date()
    }});
  }}

  public exportOpenMetrics(): string {{
    const lines: string[] = [];
    for (const p of this.points) {{
      const tagStr = Object.entries(p.tags).map(([k, v]) => `${{k}}="${{v}}"`).join(',');
      const formattedTags = tagStr ? `{{service="{svc}",${{tagStr}}}}` : `{{service="{svc}"}}`;
      lines.push(`${{p.metricName}}${{formattedTags}} ${{p.value}}`);
    }}
    return lines.join('\\n');
  }}

  public flush(): void {{
    this.points = [];
  }}
}}
"""
            write_file(f"services/{svc}/src/infrastructure/telemetry/{metrics_name.lower()}.ts", ts_code)

    # =========================================================================
    # 4. 30 Microservice Distributed Saga Transaction Step Coordinators (v4, v5, v6)
    # =========================================================================
    for svc in services:
        for idx in range(4, 7):
            saga_name = f"{svc.replace('-', '_').title().replace('_', '')}SagaStepCoordinatorV{idx}"
            ts_code = f"""import {{ Logger }} from '@novacommerce/core-logger';

export interface SagaTransactionContextV{idx} {{
  sagaId: string;
  orderId: string;
  currentStepIndex: number;
  totalSteps: number;
  isCompensating: boolean;
  compensationLog: string[];
}}

export class {saga_name} {{
  private logger: Logger;

  constructor(logger: Logger) {{
    this.logger = logger;
  }}

  public async executeForwardStep(ctx: SagaTransactionContextV{idx}, stepName: string, action: () => Promise<boolean>): Promise<boolean> {{
    this.logger.info(`Executing forward saga step [${{stepName}}] for saga ${{ctx.sagaId}} in {svc}`);
    try {{
      const success = await action();
      if (success) {{
        ctx.compensationLog.push(stepName);
        ctx.currentStepIndex++;
      }}
      return success;
    }} catch (err) {{
      this.logger.error(`Forward step [${{stepName}}] failed in {svc}:`, err);
      return false;
    }}
  }}

  public async executeCompensation(ctx: SagaTransactionContextV{idx}, compensatorMap: Record<string, () => Promise<void>>): Promise<void> {{
    this.logger.warn(`Triggering saga rollback compensation for saga ${{ctx.sagaId}} in {svc}`);
    ctx.isCompensating = true;

    // Rollback in reverse order
    const reverseSteps = [...ctx.compensationLog].reverse();
    for (const step of reverseSteps) {{
      const compFn = compensatorMap[step];
      if (compFn) {{
        this.logger.info(`Compensating step [${{step}}] in {svc}`);
        try {{
          await compFn();
        }} catch (err) {{
          this.logger.error(`Failed to compensate step [${{step}}] in {svc}:`, err);
        }}
      }}
    }}
  }}
}}
"""
            write_file(f"services/{svc}/src/domain/sagas/{saga_name.lower()}.ts", ts_code)

    # =========================================================================
    # 5. 30 Python SDK Query Models & Serialization Schemas (v4, v5, v6)
    # =========================================================================
    for svc in services:
        for idx in range(4, 7):
            model_name = f"{svc.replace('-', '_').title().replace('_', '')}ModelV{idx}"
            file_name = f"{svc.replace('-', '_')}_model_v{idx}.py"
            py_code = f"""from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class {model_name}Payload(BaseModel):
    id: str = Field(..., description="Unique entity identifier")
    tenant_id: str = Field(..., description="Multi-tenant account identifier")
    entity_code: str = Field(..., description="Alphanumeric business code")
    display_name: str = Field(..., description="Human readable name")
    status: str = Field(default="ACTIVE", description="Operating lifecycle status")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom extensible payload attributes")
    version: int = Field(default=1, description="Optimistic locking revision number")
    is_deleted: bool = Field(default=False, description="Soft deletion indicator")
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")

class {model_name}Filter(BaseModel):
    tenant_id: str
    status: Optional[str] = None
    search: Optional[str] = None
    limit: int = 20
    offset: int = 0

class {model_name}ListResponse(BaseModel):
    items: List[{model_name}Payload]
    total_count: int
    limit: int
    offset: int
    has_more: bool
"""
            write_file(f"sdks/python/novacommerce/models/{file_name}", py_code)

    print("Part 2 Generation complete.")

if __name__ == "__main__":
    generate_part2()
