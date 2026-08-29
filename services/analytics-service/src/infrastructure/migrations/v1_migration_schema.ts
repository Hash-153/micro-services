export interface MigrationSchemaV1 {
  version: number;
  serviceName: 'analytics-service';
  tableName: 'analytics_table_v1';
  upSql: string;
  downSql: string;
  rollbackSteps: string[];
}

export const MIGRATION_SCHEMA_V1: MigrationSchemaV1 = {
  version: 1,
  serviceName: 'analytics-service',
  tableName: 'analytics_table_v1',
  upSql: `
    CREATE TABLE IF NOT EXISTS analytics_table_v1 (
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
    CREATE INDEX IF NOT EXISTS idx_analytics_table_v1_tenant ON analytics_table_v1(tenant_id);
    CREATE INDEX IF NOT EXISTS idx_analytics_table_v1_status ON analytics_table_v1(status);
    CREATE INDEX IF NOT EXISTS idx_analytics_table_v1_created_at ON analytics_table_v1(created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_analytics_table_v1_metadata_gin ON analytics_table_v1 USING gin (metadata);
  `,
  downSql: `
    DROP TABLE IF EXISTS analytics_table_v1 CASCADE;
  `,
  rollbackSteps: [
    'Export table data to S3 backup archive',
    'Verify no active connections holding locks on analytics_table_v1',
    'Execute downSql within a single transactional block',
    'Update migration log registry to previous version (0)'
  ]
};

export class MigrationExecutorV1 {
  public static getUpScript(): string {
    return MIGRATION_SCHEMA_V1.upSql;
  }

  public static getDownScript(): string {
    return MIGRATION_SCHEMA_V1.downSql;
  }
}
