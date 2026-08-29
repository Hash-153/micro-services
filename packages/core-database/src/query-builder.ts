export class QueryBuilder<T = any> {
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
