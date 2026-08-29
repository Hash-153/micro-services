import { EventType } from '../enums/EventType.js';

export interface DomainEvent<T = unknown> {
  id: string;
  eventType: EventType;
  aggregateId: string;
  aggregateType: string;
  version: number;
  timestamp: string;
  correlationId: string;
  causationId?: string;
  producer: string;
  payload: T;
}

export interface OutboxEventRecord {
  id: string;
  aggregateType: string;
  aggregateId: string;
  eventType: string;
  payload: string; // JSON stringified
  correlationId: string;
  status: 'PENDING' | 'PUBLISHED' | 'FAILED';
  retryCount: number;
  lastError?: string;
  createdAt: Date;
  processedAt?: Date;
}
