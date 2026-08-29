export interface MigrationSchemaV3 {
  version: number;
  serviceName: 'user-service';
  tableName: 'user_table_v3';
  upSql: string;
  downSql: string;
  rollbackSteps: string[];
}

export const MIGRATION_SCHEMA_V3: MigrationSchemaV3 = {
  version: 3,
  serviceName: 'user-service',
  tableName: 'user_table_v3',
  upSql: `
    CREATE TABLE IF NOT EXISTS user_table_v3 (
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
    CREATE INDEX IF NOT EXISTS idx_user_table_v3_tenant ON user_table_v3(tenant_id);
    CREATE INDEX IF NOT EXISTS idx_user_table_v3_status ON user_table_v3(status);
    CREATE INDEX IF NOT EXISTS idx_user_table_v3_created_at ON user_table_v3(created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_user_table_v3_metadata_gin ON user_table_v3 USING gin (metadata);
  `,
  downSql: `
    DROP TABLE IF EXISTS user_table_v3 CASCADE;
  `,
  rollbackSteps: [
    'Export table data to S3 backup archive',
    'Verify no active connections holding locks on user_table_v3',
    'Execute downSql within a single transactional block',
    'Update migration log registry to previous version (2)'
  ]
};

export class MigrationExecutorV3 {
  public static getUpScript(): string {
    return MIGRATION_SCHEMA_V3.upSql;
  }

  public static getDownScript(): string {
    return MIGRATION_SCHEMA_V3.downSql;
  }
}
