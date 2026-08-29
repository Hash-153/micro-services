import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_massive_production_code():
    print("Beginning massive production code generation...")

    # =========================================================================
    # 1. CORE PACKAGES PRODUCTION CODE
    # =========================================================================
    
    # packages/core-types/src/contracts.ts
    write_file("packages/core-types/src/contracts.ts", """import { UserRole, OrderStatus, PaymentStatus, FulfillmentStatus, Currency, KycStatus, AccountStatus } from './enums.js';
import { Money, AddressEntity, Dimensions3D } from './domain-models.js';

export interface PaginationParams {
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export interface PaginatedResult<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
  hasNext: boolean;
  hasPrevious: boolean;
}

export interface IBaseRepository<T> {
  findById(id: string): Promise<T | null>;
  findMany(params: PaginationParams, filter?: Record<string, any>): Promise<PaginatedResult<T>>;
  create(entity: Omit<T, 'id' | 'createdAt' | 'updatedAt'>): Promise<T>;
  update(id: string, partial: Partial<T>): Promise<T>;
  delete(id: string): Promise<boolean>;
  softDelete?(id: string): Promise<boolean>;
}

export interface IUnitOfWork {
  begin(): Promise<void>;
  commit(): Promise<void>;
  rollback(): Promise<void>;
  executeInTransaction<R>(operation: () => Promise<R>): Promise<R>;
}

export interface IEventBus {
  publish<T>(topic: string, event: IDomainEvent<T>): Promise<void>;
  subscribe<T>(topic: string, handler: (event: IDomainEvent<T>) => Promise<void>): Promise<void>;
  unsubscribe(topic: string): Promise<void>;
}

export interface IDomainEvent<T = any> {
  eventId: string;
  eventType: string;
  aggregateId: string;
  aggregateType: string;
  timestamp: Date;
  correlationId: string;
  causationId?: string;
  version: number;
  payload: T;
}

export interface ISagaStep<TContext = any, TResult = any> {
  name: string;
  execute(context: TContext): Promise<TResult>;
  compensate(context: TContext): Promise<void>;
}

export interface ISagaOrchestrator<TContext = any> {
  execute(initialContext: TContext): Promise<SagaExecutionResult<TContext>>;
}

export interface SagaExecutionResult<TContext = any> {
  sagaId: string;
  status: 'COMPLETED' | 'COMPENSATED' | 'FAILED';
  finalContext: TContext;
  executedSteps: string[];
  compensatedSteps: string[];
  error?: string;
  completedAt: Date;
}
""")

    # packages/core-database/src/query-builder.ts
    write_file("packages/core-database/src/query-builder.ts", """export class QueryBuilder<T = any> {
  private tableName: string;
  private selectedFields: string[] = ['*'];
  private whereClauses: { field: string; operator: string; value: any }[] = [];
  private orderClauses: { field: string; direction: 'ASC' | 'DESC' }[] = [];
  private limitValue?: number;
  private offsetValue?: number;

  constructor(tableName: string) {
    this.tableName = tableName;
  }

  public static table<T = any>(tableName: string): QueryBuilder<T> {
    return new QueryBuilder<T>(tableName);
  }

  public select(...fields: string[]): this {
    if (fields.length > 0) {
      this.selectedFields = fields;
    }
    return this;
  }

  public where(field: string, operator: string, value: any): this {
    this.whereClauses.push({ field, operator, value });
    return this;
  }

  public whereEq(field: string, value: any): this {
    return this.where(field, '=', value);
  }

  public whereIn(field: string, values: any[]): this {
    return this.where(field, 'IN', values);
  }

  public orderBy(field: string, direction: 'ASC' | 'DESC' = 'ASC'): this {
    this.orderClauses.push({ field, direction });
    return this;
  }

  public limit(count: number): this {
    this.limitValue = count;
    return this;
  }

  public offset(count: number): this {
    this.offsetValue = count;
    return this;
  }

  public toSql(): { sql: string; values: any[] } {
    let sql = `SELECT ${this.selectedFields.join(', ')} FROM ${this.tableName}`;
    const values: any[] = [];

    if (this.whereClauses.length > 0) {
      const conditions = this.whereClauses.map((clause, idx) => {
        if (clause.operator === 'IN') {
          const placeholders = (clause.value as any[]).map(() => `$${values.length + 1}`).join(', ');
          values.push(...(clause.value as any[]));
          return `${clause.field} IN (${placeholders})`;
        } else {
          values.push(clause.value);
          return `${clause.field} ${clause.operator} $${values.length}`;
        }
      });
      sql += ` WHERE ${conditions.join(' AND ')}`;
    }

    if (this.orderClauses.length > 0) {
      const orders = this.orderClauses.map(o => `${o.field} ${o.direction}`);
      sql += ` ORDER BY ${orders.join(', ')}`;
    }

    if (this.limitValue !== undefined) {
      sql += ` LIMIT ${this.limitValue}`;
    }

    if (this.offsetValue !== undefined) {
      sql += ` OFFSET ${this.offsetValue}`;
    }

    return { sql, values };
  }
}
""")

    # packages/core-middleware/src/audit-logger.middleware.ts
    write_file("packages/core-middleware/src/audit-logger.middleware.ts", """import { Request, Response, NextFunction } from 'express';
import { Logger } from '@novacommerce/core-logger';

export interface AuditRecord {
  service: string;
  method: string;
  path: string;
  statusCode: number;
  durationMs: number;
  userId?: string;
  ipAddress?: string;
  userAgent?: string;
  correlationId?: string;
  timestamp: string;
}

export function createAuditMiddleware(serviceName: string, logger: Logger) {
  return (req: Request, res: Response, next: NextFunction) => {
    const startTime = Date.now();
    const correlationId = (req.headers['x-correlation-id'] as string) || (req as any).correlationId;

    res.on('finish', () => {
      const durationMs = Date.now() - startTime;
      const user = (req as any).user;

      const record: AuditRecord = {
        service: serviceName,
        method: req.method,
        path: req.originalUrl || req.url,
        statusCode: res.statusCode,
        durationMs,
        userId: user?.id,
        ipAddress: req.ip || req.socket.remoteAddress,
        userAgent: req.get('user-agent'),
        correlationId,
        timestamp: new Date().toISOString()
      };

      if (res.statusCode >= 400) {
        logger.warn(`[AUDIT-WARN] ${record.method} ${record.path} ${record.statusCode} - ${durationMs}ms`, record);
      } else {
        logger.info(`[AUDIT] ${record.method} ${record.path} ${record.statusCode} - ${durationMs}ms`, record);
      }
    });

    next();
  };
}
""")

    print("Generated core packages extended production components.")

if __name__ == "__main__":
    generate_massive_production_code()
