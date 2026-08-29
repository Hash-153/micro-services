import { DatabaseClient } from './index.js';
import { Logger } from '@novacommerce/core-logger';

export class ReadWriteSplitProxy {
  private primaryDb: DatabaseClient;
  private replicaDbs: DatabaseClient[];
  private logger: Logger;
  private rrIndex: number = 0;

  constructor(primaryDb: DatabaseClient, replicaDbs: DatabaseClient[], logger: Logger) {
    this.primaryDb = primaryDb;
    this.replicaDbs = replicaDbs;
    this.logger = logger;
  }

  public async query<T = any>(sql: string, params: any[] = []): Promise<T[]> {
    const trimmed = sql.trim().toUpperCase();
    const isReadOnly = trimmed.startsWith('SELECT') && !trimmed.includes('FOR UPDATE');

    if (isReadOnly && this.replicaDbs.length > 0) {
      const replica = this.replicaDbs[this.rrIndex % this.replicaDbs.length];
      this.rrIndex++;
      try {
        return await replica.query<T>(sql, params);
      } catch (err) {
        this.logger.warn('Replica read failed, falling back to primary database');
      }
    }

    return await this.primaryDb.query<T>(sql, params);
  }
}
