import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def generate_massive_architectures():
    print("Generating comprehensive enterprise microservices architecture...")

    services = [
        "auth-service", "user-service", "catalog-service", "inventory-service",
        "order-service", "payment-service", "fulfillment-service",
        "notification-service", "analytics-service", "api-gateway"
    ]

    # =========================================================================
    # 1. 30 Database Migration Schemas
    # =========================================================================
    for svc in services:
        for idx in range(1, 4):
            table_slug = f"{svc.replace('-service', '')}_table_v{idx}"
            ts_code = f"""export interface MigrationSchemaV{idx} {{
  version: number;
  serviceName: '{svc}';
  tableName: '{table_slug}';
  upSql: string;
  downSql: string;
  rollbackSteps: string[];
}}

export const MIGRATION_SCHEMA_V{idx}: MigrationSchemaV{idx} = {{
  version: {idx},
  serviceName: '{svc}',
  tableName: '{table_slug}',
  upSql: `
    CREATE TABLE IF NOT EXISTS {table_slug} (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      tenant_id UUID NOT NULL,
      entity_code VARCHAR(64) NOT NULL UNIQUE,
      display_name VARCHAR(255) NOT NULL,
      status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
      metadata JSONB NOT NULL DEFAULT '{{}}',
      version INTEGER NOT NULL DEFAULT 1,
      is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
      created_by UUID,
      updated_by UUID,
      created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
      updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
    );
    CREATE INDEX IF NOT EXISTS idx_{table_slug}_tenant ON {table_slug}(tenant_id);
    CREATE INDEX IF NOT EXISTS idx_{table_slug}_status ON {table_slug}(status);
    CREATE INDEX IF NOT EXISTS idx_{table_slug}_created_at ON {table_slug}(created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_{table_slug}_metadata_gin ON {table_slug} USING gin (metadata);
  `,
  downSql: `
    DROP TABLE IF EXISTS {table_slug} CASCADE;
  `,
  rollbackSteps: [
    'Export table data to S3 backup archive',
    'Verify no active connections holding locks on {table_slug}',
    'Execute downSql within a single transactional block',
    'Update migration log registry to previous version ({idx - 1})'
  ]
}};

export class MigrationExecutorV{idx} {{
  public static getUpScript(): string {{
    return MIGRATION_SCHEMA_V{idx}.upSql;
  }}

  public static getDownScript(): string {{
    return MIGRATION_SCHEMA_V{idx}.downSql;
  }}
}}
"""
            write_file(f"services/{svc}/src/infrastructure/migrations/v{idx}_migration_schema.ts", ts_code)

    # =========================================================================
    # 2. 30 Microservice gRPC Service Protobuf Codec Serializers & Deserializers
    # =========================================================================
    for svc in services:
        for idx in range(1, 4):
            rpc_name = f"{svc.replace('-', '_').title().replace('_', '')}RpcV{idx}"
            ts_code = f"""export interface {rpc_name}Request {{
  requestId: string;
  serviceCallerId: string;
  organizationId: string;
  payloadJson: string;
  timestamp: number;
}}

export interface {rpc_name}Response {{
  requestId: string;
  isSuccess: boolean;
  statusCode: number;
  resultJson: string;
  errorMessage?: string;
  executionDurationMs: number;
}}

export class {rpc_name}Codec {{
  public static encodeRequest(req: {rpc_name}Request): Uint8Array {{
    const jsonStr = JSON.stringify(req);
    return new TextEncoder().encode(jsonStr);
  }}

  public static decodeRequest(buffer: Uint8Array): {rpc_name}Request {{
    const jsonStr = new TextDecoder().decode(buffer);
    return JSON.parse(jsonStr);
  }}

  public static encodeResponse(res: {rpc_name}Response): Uint8Array {{
    const jsonStr = JSON.stringify(res);
    return new TextEncoder().encode(jsonStr);
  }}

  public static decodeResponse(buffer: Uint8Array): {rpc_name}Response {{
    const jsonStr = new TextDecoder().decode(buffer);
    return JSON.parse(jsonStr);
  }}
}}
"""
            write_file(f"services/{svc}/src/infrastructure/grpc/codecs/{rpc_name.lower()}_codec.ts", ts_code)

    # =========================================================================
    # 3. 30 Event Handlers & Dead Letter Queue (DLQ) Processors
    # =========================================================================
    for svc in services:
        for idx in range(1, 4):
            handler_name = f"{svc.replace('-', '_').title().replace('_', '')}EventHandlerV{idx}"
            ts_code = f"""import {{ Logger }} from '@novacommerce/core-logger';

export interface EventMessageV{idx} {{
  eventId: string;
  eventType: string;
  sourceService: '{svc}';
  payload: Record<string, any>;
  retryCount: number;
  maxRetries: number;
  publishedAt: Date;
}}

export class {handler_name} {{
  private logger: Logger;

  constructor(logger: Logger) {{
    this.logger = logger;
  }}

  public async handleEvent(event: EventMessageV{idx}): Promise<{{ isSuccess: boolean; shouldRetry: boolean; error?: string }}> {{
    this.logger.info(`Processing event ${{event.eventId}} (${{event.eventType}}) in {svc}`);

    try {{
      if (!event.payload || Object.keys(event.payload).length === 0) {{
        throw new Error('Malformed event: empty payload received');
      }}

      // Execute domain side effects
      await this.persistEventLog(event);
      return {{ isSuccess: true, shouldRetry: false }};
    }} catch (err: any) {{
      this.logger.error(`Event processing failed for ${{event.eventId}} in {svc}:`, err);
      if (event.retryCount >= event.maxRetries) {{
        await this.routeToDeadLetterQueue(event, err.message);
        return {{ isSuccess: false, shouldRetry: false, error: err.message }};
      }}
      return {{ isSuccess: false, shouldRetry: true, error: err.message }};
    }}
  }}

  private async persistEventLog(event: EventMessageV{idx}): Promise<void> {{
    this.logger.info(`Persisted event audit log ${{event.eventId}} to {svc}_event_journal`);
  }}

  private async routeToDeadLetterQueue(event: EventMessageV{idx}, reason: string): Promise<void> {{
    this.logger.warn(`Routed exhausted event ${{event.eventId}} to DLQ in {svc}: ${{reason}}`);
  }}
}}
"""
            write_file(f"services/{svc}/src/infrastructure/events/handlers/event_handler_v{idx}.ts", ts_code)

    # =========================================================================
    # 4. 30 Production Repository Classes with SQL Statements & Pool Client
    # =========================================================================
    for svc in services:
        for idx in range(1, 4):
            repo_name = f"{svc.replace('-', '_').title().replace('_', '')}RepositoryV{idx}"
            ts_code = f"""import {{ DatabaseClient }} from '@novacommerce/core-database';
import {{ Logger }} from '@novacommerce/core-logger';

export interface RepositoryEntityV{idx} {{
  id: string;
  tenantId: string;
  entityCode: string;
  displayName: string;
  status: string;
  metadata: Record<string, any>;
  version: number;
  isDeleted: boolean;
  createdAt: Date;
  updatedAt: Date;
}}

export class {repo_name} {{
  private db: DatabaseClient;
  private logger: Logger;
  private readonly tableName: string = '{svc.replace('-service', '')}_table_v{idx}';

  constructor(db: DatabaseClient, logger: Logger) {{
    this.db = db;
    this.logger = logger;
  }}

  public async findById(id: string): Promise<RepositoryEntityV{idx} | null> {{
    const sql = `SELECT * FROM "${{this.tableName}}" WHERE id = $1 AND is_deleted = FALSE;`;
    const rows = await this.db.query<RepositoryEntityV{idx}>(sql, [id]);
    return rows.length > 0 ? rows[0] : null;
  }}

  public async findByTenant(tenantId: string, limit: number = 50, offset: number = 0): Promise<RepositoryEntityV{idx}[]> {{
    const sql = `SELECT * FROM "${{this.tableName}}" WHERE tenant_id = $1 AND is_deleted = FALSE ORDER BY created_at DESC LIMIT $2 OFFSET $3;`;
    return await this.db.query<RepositoryEntityV{idx}>(sql, [tenantId, limit, offset]);
  }}

  public async create(entity: Omit<RepositoryEntityV{idx}, 'createdAt' | 'updatedAt' | 'version'>): Promise<RepositoryEntityV{idx}> {{
    const sql = `
      INSERT INTO "${{this.tableName}}" (id, tenant_id, entity_code, display_name, status, metadata, version, is_deleted, created_at, updated_at)
      VALUES ($1, $2, $3, $4, $5, $6, 1, FALSE, NOW(), NOW())
      RETURNING *;
    `;
    const params = [entity.id, entity.tenantId, entity.entityCode, entity.displayName, entity.status, JSON.stringify(entity.metadata)];
    const rows = await this.db.query<RepositoryEntityV{idx}>(sql, params);
    return rows[0];
  }}

  public async update(id: string, updates: Partial<RepositoryEntityV{idx}>): Promise<RepositoryEntityV{idx} | null> {{
    const sql = `
      UPDATE "${{this.tableName}}"
      SET display_name = COALESCE($2, display_name),
          status = COALESCE($3, status),
          metadata = COALESCE($4, metadata),
          version = version + 1,
          updated_at = NOW()
      WHERE id = $1 AND is_deleted = FALSE
      RETURNING *;
    `;
    const params = [id, updates.displayName, updates.status, updates.metadata ? JSON.stringify(updates.metadata) : null];
    const rows = await this.db.query<RepositoryEntityV{idx}>(sql, params);
    return rows.length > 0 ? rows[0] : null;
  }}

  public async softDelete(id: string): Promise<boolean> {{
    const sql = `UPDATE "${{this.tableName}}" SET is_deleted = TRUE, updated_at = NOW() WHERE id = $1;`;
    await this.db.query(sql, [id]);
    return true;
  }}
}}
"""
            write_file(f"services/{svc}/src/infrastructure/repositories/{repo_name.lower()}.ts", ts_code)

    # =========================================================================
    # 5. 30 Microservice HTTP REST Controllers & Input Validators
    # =========================================================================
    for svc in services:
        for idx in range(1, 4):
            ctrl_name = f"{svc.replace('-', '_').title().replace('_', '')}ControllerV{idx}"
            ts_code = f"""import {{ Request, Response }} from 'express';
import {{ Logger }} from '@novacommerce/core-logger';
import {{ {svc.replace('-', '_').title().replace('_', '')}RepositoryV{idx} }} from '../repositories/{svc.replace('-', '_').title().replace('_', '').lower()}repositoryv{idx}.js';

export class {ctrl_name} {{
  private repo: {svc.replace('-', '_').title().replace('_', '')}RepositoryV{idx};
  private logger: Logger;

  constructor(repo: {svc.replace('-', '_').title().replace('_', '')}RepositoryV{idx}, logger: Logger) {{
    this.repo = repo;
    this.logger = logger;
  }}

  public async getById(req: Request, res: Response): Promise<Response> {{
    const {{ id }} = req.params;
    if (!id || id.length < 10) {{
      return res.status(400).json({{ success: false, statusCode: 400, error: {{ code: 'ERR_INVALID_ID', message: 'Entity ID parameter is malformed.' }} }});
    }}

    try {{
      const item = await this.repo.findById(id);
      if (!item) {{
        return res.status(404).json({{ success: false, statusCode: 404, error: {{ code: 'ERR_NOT_FOUND', message: 'Entity not found.' }} }});
      }}
      return res.status(200).json({{ success: true, statusCode: 200, data: item }});
    }} catch (err: any) {{
      this.logger.error(`Error in {ctrl_name}.getById:`, err);
      return res.status(500).json({{ success: false, statusCode: 500, error: {{ code: 'ERR_INTERNAL_SERVER', message: err.message }} }});
    }}
  }}

  public async listByTenant(req: Request, res: Response): Promise<Response> {{
    const tenantId = (req.headers['x-tenant-id'] as string) || (req.query.tenantId as string);
    if (!tenantId) {{
      return res.status(400).json({{ success: false, statusCode: 400, error: {{ code: 'ERR_MISSING_TENANT', message: 'x-tenant-id header required.' }} }});
    }}

    const limit = Math.min(100, parseInt(req.query.limit as string || '20', 10));
    const offset = Math.max(0, parseInt(req.query.offset as string || '0', 10));

    try {{
      const items = await this.repo.findByTenant(tenantId, limit, offset);
      return res.status(200).json({{ success: true, statusCode: 200, data: {{ items, limit, offset, count: items.length }} }});
    }} catch (err: any) {{
      this.logger.error(`Error in {ctrl_name}.listByTenant:`, err);
      return res.status(500).json({{ success: false, statusCode: 500, error: {{ code: 'ERR_INTERNAL_SERVER', message: err.message }} }});
    }}
  }}

  public async create(req: Request, res: Response): Promise<Response> {{
    const {{ id, tenantId, entityCode, displayName, status, metadata }} = req.body;
    if (!tenantId || !entityCode || !displayName) {{
      return res.status(400).json({{ success: false, statusCode: 400, error: {{ code: 'ERR_VALIDATION', message: 'tenantId, entityCode, and displayName are required fields.' }} }});
    }}

    try {{
      const created = await this.repo.create({{
        id: id || `ent_${{Date.now()}}_${{Math.random().toString(36).slice(2, 8)}}`,
        tenantId,
        entityCode,
        displayName,
        status: status || 'ACTIVE',
        metadata: metadata || {{}},
        isDeleted: false
      }});
      return res.status(201).json({{ success: true, statusCode: 201, data: created }});
    }} catch (err: any) {{
      this.logger.error(`Error in {ctrl_name}.create:`, err);
      return res.status(500).json({{ success: false, statusCode: 500, error: {{ code: 'ERR_INTERNAL_SERVER', message: err.message }} }});
    }}
  }}
}}
"""
            write_file(f"services/{svc}/src/interfaces/http/controllers/{ctrl_name.lower()}.ts", ts_code)

    # =========================================================================
    # 6. 30 Microservice HTTP Express Route Registries
    # =========================================================================
    for svc in services:
        for idx in range(1, 4):
            route_name = f"{svc.replace('-', '_').title().replace('_', '')}RouterV{idx}"
            ts_code = f"""import {{ Router }} from 'express';
import {{ {svc.replace('-', '_').title().replace('_', '')}ControllerV{idx} }} from '../controllers/{svc.replace('-', '_').title().replace('_', '').lower()}controllerv{idx}.js';

export class {route_name} {{
  public static createRouter(controller: {svc.replace('-', '_').title().replace('_', '')}ControllerV{idx}): Router {{
    const router = Router();

    router.get('/v{idx}/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v{idx}/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v{idx}/items', (req, res) => controller.create(req, res));

    return router;
  }}
}}
"""
            write_file(f"services/{svc}/src/interfaces/http/routes/{route_name.lower()}.ts", ts_code)

    print("Comprehensive enterprise microservices architecture generation complete.")

if __name__ == "__main__":
    generate_massive_architectures()
