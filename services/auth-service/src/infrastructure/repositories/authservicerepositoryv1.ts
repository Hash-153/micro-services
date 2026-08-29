import { DatabaseClient } from '@novacommerce/core-database';
import { Logger } from '@novacommerce/core-logger';

export interface RepositoryEntityV1 {
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
}

export class AuthServiceRepositoryV1 {
  private db: DatabaseClient;
  private logger: Logger;
  private readonly tableName: string = 'auth_table_v1';

  constructor(db: DatabaseClient, logger: Logger) {
    this.db = db;
    this.logger = logger;
  }

  public async findById(id: string): Promise<RepositoryEntityV1 | null> {
    const sql = `SELECT * FROM "${this.tableName}" WHERE id = $1 AND is_deleted = FALSE;`;
    const rows = await this.db.query<RepositoryEntityV1>(sql, [id]);
    return rows.length > 0 ? rows[0] : null;
  }

  public async findByTenant(tenantId: string, limit: number = 50, offset: number = 0): Promise<RepositoryEntityV1[]> {
    const sql = `SELECT * FROM "${this.tableName}" WHERE tenant_id = $1 AND is_deleted = FALSE ORDER BY created_at DESC LIMIT $2 OFFSET $3;`;
    return await this.db.query<RepositoryEntityV1>(sql, [tenantId, limit, offset]);
  }

  public async create(entity: Omit<RepositoryEntityV1, 'createdAt' | 'updatedAt' | 'version'>): Promise<RepositoryEntityV1> {
    const sql = `
      INSERT INTO "${this.tableName}" (id, tenant_id, entity_code, display_name, status, metadata, version, is_deleted, created_at, updated_at)
      VALUES ($1, $2, $3, $4, $5, $6, 1, FALSE, NOW(), NOW())
      RETURNING *;
    `;
    const params = [entity.id, entity.tenantId, entity.entityCode, entity.displayName, entity.status, JSON.stringify(entity.metadata)];
    const rows = await this.db.query<RepositoryEntityV1>(sql, params);
    return rows[0];
  }

  public async update(id: string, updates: Partial<RepositoryEntityV1>): Promise<RepositoryEntityV1 | null> {
    const sql = `
      UPDATE "${this.tableName}"
      SET display_name = COALESCE($2, display_name),
          status = COALESCE($3, status),
          metadata = COALESCE($4, metadata),
          version = version + 1,
          updated_at = NOW()
      WHERE id = $1 AND is_deleted = FALSE
      RETURNING *;
    `;
    const params = [id, updates.displayName, updates.status, updates.metadata ? JSON.stringify(updates.metadata) : null];
    const rows = await this.db.query<RepositoryEntityV1>(sql, params);
    return rows.length > 0 ? rows[0] : null;
  }

  public async softDelete(id: string): Promise<boolean> {
    const sql = `UPDATE "${this.tableName}" SET is_deleted = TRUE, updated_at = NOW() WHERE id = $1;`;
    await this.db.query(sql, [id]);
    return true;
  }
}
