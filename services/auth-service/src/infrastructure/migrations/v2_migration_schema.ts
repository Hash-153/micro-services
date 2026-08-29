export interface MigrationSchemaV2 {
  version: number;
  serviceName: 'auth-service';
  tableName: 'auth_table_v2';
  upSql: string;
  downSql: string;
  rollbackSteps: string[];
}

export const MIGRATION_SCHEMA_V2: MigrationSchemaV2 = {
  version: 2,
  serviceName: 'auth-service',
  tableName: 'auth_table_v2',
  upSql: `
    CREATE TABLE IF NOT EXISTS auth_table_v2 (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      tenant_id UUID NOT NULL,
      entity_code VARCHAR(64) NOT NULL UNIQUE,
      display_name VARCHAR(255) NOT NULL,
      status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
      metadata JSONB NOT NULL DEFAULT '{}',
      version INTEGER NOT NULL DEFAULT 1,
      is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
      created_by UUID,
      updated_by UUID,
      created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
      updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
    );
    CREATE INDEX IF NOT EXISTS idx_auth_table_v2_tenant ON auth_table_v2(tenant_id);
    CREATE INDEX IF NOT EXISTS idx_auth_table_v2_status ON auth_table_v2(status);
    CREATE INDEX IF NOT EXISTS idx_auth_table_v2_created_at ON auth_table_v2(created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_auth_table_v2_metadata_gin ON auth_table_v2 USING gin (metadata);
  `,
  downSql: `
    DROP TABLE IF EXISTS auth_table_v2 CASCADE;
  `,
  rollbackSteps: [
    'Export table data to S3 backup archive',
    'Verify no active connections holding locks on auth_table_v2',
    'Execute downSql within a single transactional block',
    'Update migration log registry to previous version (1)'
  ]
};

export class MigrationExecutorV2 {
  public static getUpScript(): string {
    return MIGRATION_SCHEMA_V2.upSql;
  }

  public static getDownScript(): string {
    return MIGRATION_SCHEMA_V2.downSql;
  }
}
