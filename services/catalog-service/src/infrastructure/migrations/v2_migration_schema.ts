export interface MigrationSchemaV2 {
  version: number;
  serviceName: 'catalog-service';
  tableName: 'catalog_table_v2';
  upSql: string;
  downSql: string;
  rollbackSteps: string[];
}

export const MIGRATION_SCHEMA_V2: MigrationSchemaV2 = {
  version: 2,
  serviceName: 'catalog-service',
  tableName: 'catalog_table_v2',
  upSql: `
    CREATE TABLE IF NOT EXISTS catalog_table_v2 (
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
    CREATE INDEX IF NOT EXISTS idx_catalog_table_v2_tenant ON catalog_table_v2(tenant_id);
    CREATE INDEX IF NOT EXISTS idx_catalog_table_v2_status ON catalog_table_v2(status);
    CREATE INDEX IF NOT EXISTS idx_catalog_table_v2_created_at ON catalog_table_v2(created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_catalog_table_v2_metadata_gin ON catalog_table_v2 USING gin (metadata);
  `,
  downSql: `
    DROP TABLE IF EXISTS catalog_table_v2 CASCADE;
  `,
  rollbackSteps: [
    'Export table data to S3 backup archive',
    'Verify no active connections holding locks on catalog_table_v2',
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
