export interface IBaseRepository<T, ID = string> {
  findById(id: ID): Promise<T | null>;
  findAll(filter?: Partial<T>, limit?: number, offset?: number): Promise<T[]>;
  create(entity: T): Promise<T>;
  update(id: ID, entity: Partial<T>): Promise<T | null>;
  delete(id: ID): Promise<boolean>;
  count(filter?: Partial<T>): Promise<number>;
}

export abstract class InMemoryBaseRepository<T extends { id: string }, ID = string> implements IBaseRepository<T, ID> {
  protected items: Map<string, T> = new Map();

  public async findById(id: ID): Promise<T | null> {
    const item = this.items.get(String(id));
    return item ? JSON.parse(JSON.stringify(item)) : null;
  }

  public async findAll(filter?: Partial<T>, limit: number = 50, offset: number = 0): Promise<T[]> {
    let result = Array.from(this.items.values());
    if (filter) {
      result = result.filter(item => {
        for (const [k, v] of Object.entries(filter)) {
          if ((item as any)[k] !== v) return false;
        }
        return true;
      });
    }
    return result.slice(offset, offset + limit).map(item => JSON.parse(JSON.stringify(item)));
  }

  public async create(entity: T): Promise<T> {
    const clone = JSON.parse(JSON.stringify(entity));
    this.items.set(entity.id, clone);
    return JSON.parse(JSON.stringify(clone));
  }

  public async update(id: ID, partial: Partial<T>): Promise<T | null> {
    const existing = this.items.get(String(id));
    if (!existing) return null;
    const updated = { ...existing, ...partial, updatedAt: new Date() };
    this.items.set(String(id), updated);
    return JSON.parse(JSON.stringify(updated));
  }

  public async delete(id: ID): Promise<boolean> {
    return this.items.delete(String(id));
  }

  public async count(filter?: Partial<T>): Promise<number> {
    const all = await this.findAll(filter, 1000000, 0);
    return all.length;
  }
}
