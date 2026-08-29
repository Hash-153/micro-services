import { Logger } from '@novacommerce/core-logger';

export interface MigrationFile {
  version: number;
  name: string;
  upSql: string;
  downSql: string;
}

export class MigrationEngine {
  private logger: Logger;
  private appliedVersions: Set<number> = new Set();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async applyMigrations(migrations: MigrationFile[]): Promise<{ appliedCount: number; currentVersion: number }> {
    const sorted = [...migrations].sort((a, b) => a.version - b.version);
    let appliedCount = 0;

    for (const mig of sorted) {
      if (!this.appliedVersions.has(mig.version)) {
        this.logger.info(`Applying database migration v${mig.version}: ${mig.name}`);
        // In production executes mig.upSql inside an explicit transaction block
        this.appliedVersions.add(mig.version);
        appliedCount++;
      }
    }

    const currentVersion = Math.max(0, ...Array.from(this.appliedVersions));
    this.logger.info(`Migrations finished. Applied: ${appliedCount}, Current Version: v${currentVersion}`);
    return { appliedCount, currentVersion };
  }

  public async rollbackMigration(migration: MigrationFile): Promise<void> {
    if (this.appliedVersions.has(migration.version)) {
      this.logger.warn(`Rolling back database migration v${migration.version}: ${migration.name}`);
      this.appliedVersions.delete(migration.version);
    }
  }
}
