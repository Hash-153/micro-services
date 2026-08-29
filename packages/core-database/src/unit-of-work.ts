export interface IUnitOfWork {
  start(): Promise<void>;
  commit(): Promise<void>;
  rollback(): Promise<void>;
  isActive(): boolean;
}

export class InMemoryUnitOfWork implements IUnitOfWork {
  private active: boolean = false;

  public async start(): Promise<void> {
    this.active = true;
  }

  public async commit(): Promise<void> {
    this.active = false;
  }

  public async rollback(): Promise<void> {
    this.active = false;
  }

  public isActive(): boolean {
    return this.active;
  }
}
