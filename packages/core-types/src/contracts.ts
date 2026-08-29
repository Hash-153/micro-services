import { UserRole, OrderStatus, PaymentStatus, FulfillmentStatus, Currency, KycStatus, AccountStatus } from './enums.js';
import { Money, AddressEntity, Dimensions3D } from './domain-models.js';

export interface PaginationParams {
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export interface PaginatedResult<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
  hasNext: boolean;
  hasPrevious: boolean;
}

export interface IBaseRepository<T> {
  findById(id: string): Promise<T | null>;
  findMany(params: PaginationParams, filter?: Record<string, any>): Promise<PaginatedResult<T>>;
  create(entity: Omit<T, 'id' | 'createdAt' | 'updatedAt'>): Promise<T>;
  update(id: string, partial: Partial<T>): Promise<T>;
  delete(id: string): Promise<boolean>;
  softDelete?(id: string): Promise<boolean>;
}

export interface IUnitOfWork {
  begin(): Promise<void>;
  commit(): Promise<void>;
  rollback(): Promise<void>;
  executeInTransaction<R>(operation: () => Promise<R>): Promise<R>;
}

export interface IEventBus {
  publish<T>(topic: string, event: IDomainEvent<T>): Promise<void>;
  subscribe<T>(topic: string, handler: (event: IDomainEvent<T>) => Promise<void>): Promise<void>;
  unsubscribe(topic: string): Promise<void>;
}

export interface IDomainEvent<T = any> {
  eventId: string;
  eventType: string;
  aggregateId: string;
  aggregateType: string;
  timestamp: Date;
  correlationId: string;
  causationId?: string;
  version: number;
  payload: T;
}

export interface ISagaStep<TContext = any, TResult = any> {
  name: string;
  execute(context: TContext): Promise<TResult>;
  compensate(context: TContext): Promise<void>;
}

export interface ISagaOrchestrator<TContext = any> {
  execute(initialContext: TContext): Promise<SagaExecutionResult<TContext>>;
}

export interface SagaExecutionResult<TContext = any> {
  sagaId: string;
  status: 'COMPLETED' | 'COMPENSATED' | 'FAILED';
  finalContext: TContext;
  executedSteps: string[];
  compensatedSteps: string[];
  error?: string;
  completedAt: Date;
}
