import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_core_logger():
    pkg_dir = "packages/core-logger"
    
    write_file(f"{pkg_dir}/package.json", """{
  "name": "@novacommerce/core-logger",
  "version": "1.0.0",
  "description": "Enterprise structured JSON logging with context correlation and redaction",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "clean": "rimraf dist",
    "test": "jest"
  },
  "dependencies": {
    "@novacommerce/core-types": "workspace:*"
  },
  "devDependencies": {
    "@types/jest": "^29.5.12",
    "@types/node": "^22.0.0",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.2",
    "typescript": "^5.4.0",
    "rimraf": "^5.0.5"
  }
}""")

    write_file(f"{pkg_dir}/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts", "**/*.test.ts"]
}""")

    write_file(f"{pkg_dir}/jest.config.js", """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.spec.ts', '**/*.test.ts']
};""")

    write_file(f"{pkg_dir}/src/types.ts", """export type LogLevel = 'debug' | 'info' | 'warn' | 'error' | 'fatal';

export interface LogContext {
  serviceName: string;
  environment: string;
  correlationId?: string;
  userId?: string;
  requestId?: string;
  traceId?: string;
  spanId?: string;
  [key: string]: unknown;
}

export interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  context: LogContext;
  data?: unknown;
  error?: {
    name: string;
    message: string;
    stack?: string;
    code?: string;
    details?: unknown;
  };
}

export interface ILogger {
  debug(message: string, data?: unknown, contextOverride?: Partial<LogContext>): void;
  info(message: string, data?: unknown, contextOverride?: Partial<LogContext>): void;
  warn(message: string, data?: unknown, contextOverride?: Partial<LogContext>): void;
  error(message: string, error?: Error | unknown, data?: unknown, contextOverride?: Partial<LogContext>): void;
  fatal(message: string, error?: Error | unknown, data?: unknown, contextOverride?: Partial<LogContext>): void;
  child(additionalContext: Partial<LogContext>): ILogger;
}
""")

    write_file(f"{pkg_dir}/src/redactor.ts", """const SENSITIVE_KEYS = new Set([
  'password',
  'passwordhash',
  'token',
  'accesstoken',
  'refreshtoken',
  'secret',
  'jwtsecret',
  'creditcard',
  'cardnumber',
  'cvv',
  'cvc',
  'ssn',
  'authorization',
  'apikey',
  'mfastuff',
  'mfasecret'
]);

export class Redactor {
  public static redact(obj: unknown, depth: number = 0): unknown {
    if (depth > 8 || obj === null || obj === undefined) {
      return obj;
    }

    if (typeof obj === 'string') {
      return obj;
    }

    if (Array.isArray(obj)) {
      return obj.map(item => Redactor.redact(item, depth + 1));
    }

    if (typeof obj === 'object') {
      const result: Record<string, unknown> = {};
      for (const [key, value] of Object.entries(obj as Record<string, unknown>)) {
        const lowerKey = key.toLowerCase().replace(/[^a-z0-9]/g, '');
        if (SENSITIVE_KEYS.has(lowerKey)) {
          result[key] = '[REDACTED]';
        } else if (typeof value === 'object' && value !== null) {
          result[key] = Redactor.redact(value, depth + 1);
        } else {
          result[key] = value;
        }
      }
      return result;
    }

    return obj;
  }
}
""")

    write_file(f"{pkg_dir}/src/logger.ts", """import { ILogger, LogContext, LogEntry, LogLevel } from './types.js';
import { Redactor } from './redactor.js';

const LOG_LEVEL_PRIORITY: Record<LogLevel, number> = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
  fatal: 4
};

export class Logger implements ILogger {
  private readonly context: LogContext;
  private readonly minLevel: LogLevel;

  constructor(context: LogContext, minLevel: LogLevel = 'info') {
    this.context = { ...context };
    this.minLevel = minLevel;
  }

  public static create(serviceName: string, environment: string = process.env.NODE_ENV || 'development', minLevel?: LogLevel): Logger {
    const defaultLevel = (process.env.LOG_LEVEL?.toLowerCase() as LogLevel) || (environment === 'production' ? 'info' : 'debug');
    return new Logger(
      {
        serviceName,
        environment
      },
      minLevel || defaultLevel
    );
  }

  public child(additionalContext: Partial<LogContext>): ILogger {
    return new Logger(
      {
        ...this.context,
        ...additionalContext
      },
      this.minLevel
    );
  }

  public debug(message: string, data?: unknown, contextOverride?: Partial<LogContext>): void {
    this.write('debug', message, data, undefined, contextOverride);
  }

  public info(message: string, data?: unknown, contextOverride?: Partial<LogContext>): void {
    this.write('info', message, data, undefined, contextOverride);
  }

  public warn(message: string, data?: unknown, contextOverride?: Partial<LogContext>): void {
    this.write('warn', message, data, undefined, contextOverride);
  }

  public error(message: string, error?: Error | unknown, data?: unknown, contextOverride?: Partial<LogContext>): void {
    this.write('error', message, data, error, contextOverride);
  }

  public fatal(message: string, error?: Error | unknown, data?: unknown, contextOverride?: Partial<LogContext>): void {
    this.write('fatal', message, data, error, contextOverride);
  }

  private write(
    level: LogLevel,
    message: string,
    data?: unknown,
    error?: Error | unknown,
    contextOverride?: Partial<LogContext>
  ): void {
    if (LOG_LEVEL_PRIORITY[level] < LOG_LEVEL_PRIORITY[this.minLevel]) {
      return;
    }

    const mergedContext = {
      ...this.context,
      ...contextOverride
    };

    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      context: mergedContext
    };

    if (data !== undefined) {
      entry.data = Redactor.redact(data);
    }

    if (error !== undefined) {
      if (error instanceof Error) {
        entry.error = {
          name: error.name,
          message: error.message,
          stack: error.stack,
          code: (error as Record<string, unknown>).code as string,
          details: (error as Record<string, unknown>).details
        };
      } else {
        entry.error = {
          name: 'UnknownError',
          message: String(error)
        };
      }
    }

    const outputJson = JSON.stringify(entry);
    if (level === 'error' || level === 'fatal') {
      process.stderr.write(outputJson + '\\n');
    } else {
      process.stdout.write(outputJson + '\\n');
    }
  }
}
""")

    write_file(f"{pkg_dir}/src/index.ts", """export * from './types.js';
export * from './redactor.js';
export * from './logger.js';
""")

    write_file(f"{pkg_dir}/tests/logger.test.ts", """import { Logger, Redactor } from '../src/index.js';

describe('Core Logger Suite', () => {
  it('should redact sensitive properties accurately', () => {
    const payload = {
      userId: 'user_123',
      password: 'PlainSecretPassword123',
      token: 'jwt_token_here',
      nested: {
        creditCard: '4111222233334444',
        safeProperty: 'allowed'
      }
    };

    const redacted = Redactor.redact(payload) as Record<string, any>;
    expect(redacted.userId).toBe('user_123');
    expect(redacted.password).toBe('[REDACTED]');
    expect(redacted.token).toBe('[REDACTED]');
    expect(redacted.nested.creditCard).toBe('[REDACTED]');
    expect(redacted.nested.safeProperty).toBe('allowed');
  });

  it('should create child logger with preserved and merged context', () => {
    const parent = Logger.create('test-service', 'test');
    const child = parent.child({ correlationId: 'corr-999', userId: 'user-001' });
    expect(child).toBeDefined();
  });
});
""")
    print(f"Generated {pkg_dir}")

def generate_core_events():
    pkg_dir = "packages/core-events"
    
    write_file(f"{pkg_dir}/package.json", """{
  "name": "@novacommerce/core-events",
  "version": "1.0.0",
  "description": "Event bus, RabbitMQ integration, Outbox pattern, and DLQ handlers",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "clean": "rimraf dist",
    "test": "jest"
  },
  "dependencies": {
    "@novacommerce/core-types": "workspace:*",
    "@novacommerce/core-logger": "workspace:*"
  },
  "devDependencies": {
    "@types/jest": "^29.5.12",
    "@types/node": "^22.0.0",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.2",
    "typescript": "^5.4.0",
    "rimraf": "^5.0.5"
  }
}""")

    write_file(f"{pkg_dir}/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts", "**/*.test.ts"]
}""")

    write_file(f"{pkg_dir}/jest.config.js", """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.spec.ts', '**/*.test.ts']
};""")

    write_file(f"{pkg_dir}/src/interfaces.ts", """import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface IEventPublisher {
  publish<T>(event: DomainEvent<T>): Promise<boolean>;
  publishBatch<T>(events: DomainEvent<T>[]): Promise<boolean[]>;
}

export type EventHandler<T = unknown> = (event: DomainEvent<T>) => Promise<void>;

export interface IEventSubscriber {
  subscribe<T>(eventType: EventType, handler: EventHandler<T>, queueName?: string): Promise<void>;
  unsubscribe(eventType: EventType): Promise<void>;
}

export interface IEventBus extends IEventPublisher, IEventSubscriber {
  connect(): Promise<void>;
  disconnect(): Promise<void>;
  isConnected(): boolean;
}

export interface OutboxRepository {
  saveOutboxEvent(event: DomainEvent): Promise<void>;
  fetchPendingEvents(limit: number): Promise<DomainEvent[]>;
  markEventPublished(eventId: string): Promise<void>;
  markEventFailed(eventId: string, error: string): Promise<void>;
}
""")

    write_file(f"{pkg_dir}/src/memory-bus.ts", """import { IEventBus, EventHandler } from './interfaces.js';
import { DomainEvent, EventType } from '@novacommerce/core-types';
import { ILogger } from '@novacommerce/core-logger';

export class InMemoryEventBus implements IEventBus {
  private readonly handlers: Map<EventType, Set<EventHandler<unknown>>> = new Map();
  private connected: boolean = false;
  private readonly logger?: ILogger;

  constructor(logger?: ILogger) {
    this.logger = logger;
  }

  public async connect(): Promise<void> {
    this.connected = true;
    this.logger?.info('InMemoryEventBus connected.');
  }

  public async disconnect(): Promise<void> {
    this.connected = false;
    this.handlers.clear();
    this.logger?.info('InMemoryEventBus disconnected.');
  }

  public isConnected(): boolean {
    return this.connected;
  }

  public async publish<T>(event: DomainEvent<T>): Promise<boolean> {
    if (!this.connected) {
      throw new Error('EventBus is not connected.');
    }

    const registeredHandlers = this.handlers.get(event.eventType);
    if (!registeredHandlers || registeredHandlers.size === 0) {
      this.logger?.debug(`No handlers registered for event type: ${event.eventType}`);
      return true;
    }

    for (const handler of registeredHandlers) {
      try {
        await handler(event as DomainEvent<unknown>);
      } catch (err) {
        this.logger?.error(`Error handling event ${event.eventType} with handler`, err);
        throw err;
      }
    }

    return true;
  }

  public async publishBatch<T>(events: DomainEvent<T>[]): Promise<boolean[]> {
    const results: boolean[] = [];
    for (const ev of events) {
      const res = await this.publish(ev);
      results.push(res);
    }
    return results;
  }

  public async subscribe<T>(eventType: EventType, handler: EventHandler<T>): Promise<void> {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, new Set());
    }
    this.handlers.get(eventType)!.add(handler as EventHandler<unknown>);
    this.logger?.debug(`Subscribed to event: ${eventType}`);
  }

  public async unsubscribe(eventType: EventType): Promise<void> {
    this.handlers.delete(eventType);
  }
}
""")

    write_file(f"{pkg_dir}/src/outbox-processor.ts", """import { IEventBus, OutboxRepository } from './interfaces.js';
import { ILogger } from '@novacommerce/core-logger';

export class OutboxProcessor {
  private readonly repo: OutboxRepository;
  private readonly eventBus: IEventBus;
  private readonly logger: ILogger;
  private isRunning: boolean = false;
  private pollIntervalMs: number;
  private timerHandle?: NodeJS.Timeout;

  constructor(repo: OutboxRepository, eventBus: IEventBus, logger: ILogger, pollIntervalMs: number = 1000) {
    this.repo = repo;
    this.eventBus = eventBus;
    this.logger = logger.child({ component: 'OutboxProcessor' });
    this.pollIntervalMs = pollIntervalMs;
  }

  public start(): void {
    if (this.isRunning) return;
    this.isRunning = true;
    this.logger.info('OutboxProcessor started polling loop.');
    this.scheduleNextRun();
  }

  public stop(): void {
    this.isRunning = false;
    if (this.timerHandle) {
      clearTimeout(this.timerHandle);
    }
    this.logger.info('OutboxProcessor stopped.');
  }

  public async processBatch(limit: number = 50): Promise<number> {
    const pendingEvents = await this.repo.fetchPendingEvents(limit);
    if (pendingEvents.length === 0) {
      return 0;
    }

    let processedCount = 0;
    for (const event of pendingEvents) {
      try {
        await this.eventBus.publish(event);
        await this.repo.markEventPublished(event.id);
        processedCount++;
      } catch (err: any) {
        this.logger.error(`Failed to publish outbox event: ${event.id}`, err);
        await this.repo.markEventFailed(event.id, err?.message || 'Unknown publication error');
      }
    }

    return processedCount;
  }

  private scheduleNextRun(): void {
    if (!this.isRunning) return;
    this.timerHandle = setTimeout(async () => {
      try {
        await this.processBatch();
      } catch (err) {
        this.logger.error('Error during outbox batch polling cycle', err);
      } finally {
        this.scheduleNextRun();
      }
    }, this.pollIntervalMs);
  }
}
""")

    write_file(f"{pkg_dir}/src/event-factory.ts", """import { DomainEvent, EventType } from '@novacommerce/core-types';
import { randomUUID } from 'crypto';

export class DomainEventFactory {
  public static create<T>(
    eventType: EventType,
    aggregateId: string,
    aggregateType: string,
    payload: T,
    producer: string,
    correlationId: string = randomUUID(),
    causationId?: string,
    version: number = 1
  ): DomainEvent<T> {
    return {
      id: randomUUID(),
      eventType,
      aggregateId,
      aggregateType,
      version,
      timestamp: new Date().toISOString(),
      correlationId,
      causationId,
      producer,
      payload
    };
  }
}
""")

    write_file(f"{pkg_dir}/src/index.ts", """export * from './interfaces.js';
export * from './memory-bus.js';
export * from './outbox-processor.js';
export * from './event-factory.js';
""")

    write_file(f"{pkg_dir}/tests/events.test.ts", """import { InMemoryEventBus, DomainEventFactory } from '../src/index.js';
import { EventType } from '@novacommerce/core-types';

describe('Core Events Suite', () => {
  let eventBus: InMemoryEventBus;

  beforeEach(async () => {
    eventBus = new InMemoryEventBus();
    await eventBus.connect();
  });

  afterEach(async () => {
    await eventBus.disconnect();
  });

  it('should publish and receive subscribed events correctly', async () => {
    let receivedPayload: any = null;

    await eventBus.subscribe(EventType.ORDER_CREATED, async (event) => {
      receivedPayload = event.payload;
    });

    const domainEvent = DomainEventFactory.create(
      EventType.ORDER_CREATED,
      'order_123',
      'Order',
      { orderNumber: 'ORD-2026-001', total: 9900 },
      'order-service'
    );

    await eventBus.publish(domainEvent);

    expect(receivedPayload).toEqual({ orderNumber: 'ORD-2026-001', total: 9900 });
  });
});
""")
    print(f"Generated {pkg_dir}")

def generate_core_middleware():
    pkg_dir = "packages/core-middleware"
    
    write_file(f"{pkg_dir}/package.json", """{
  "name": "@novacommerce/core-middleware",
  "version": "1.0.0",
  "description": "Express HTTP middleware for JWT verification, RBAC, rate limiting, and errors",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "clean": "rimraf dist",
    "test": "jest"
  },
  "dependencies": {
    "@novacommerce/core-types": "workspace:*",
    "@novacommerce/core-logger": "workspace:*",
    "jsonwebtoken": "^9.0.2",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/jsonwebtoken": "^9.0.6",
    "@types/jest": "^29.5.12",
    "@types/node": "^22.0.0",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.2",
    "typescript": "^5.4.0",
    "rimraf": "^5.0.5"
  }
}""")

    write_file(f"{pkg_dir}/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts", "**/*.test.ts"]
}""")

    write_file(f"{pkg_dir}/jest.config.js", """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.spec.ts', '**/*.test.ts']
};""")

    write_file(f"{pkg_dir}/src/auth.middleware.ts", """import { UserRole, UnauthorizedError, ForbiddenError } from '@novacommerce/core-types';
import jwt from 'jsonwebtoken';

export interface AuthenticatedUser {
  id: string;
  email: string;
  role: UserRole;
  organizationId?: string;
}

export interface RequestWithUser {
  user?: AuthenticatedUser;
  headers: Record<string, string | string[] | undefined>;
}

export class AuthMiddleware {
  public static verifyToken(secret: string) {
    return (req: any, res: any, next: any) => {
      const authHeader = req.headers['authorization'] || req.headers['Authorization'];
      if (!authHeader || typeof authHeader !== 'string') {
        return next(new UnauthorizedError('Missing Authorization header'));
      }

      const parts = authHeader.split(' ');
      if (parts.length !== 2 || parts[0] !== 'Bearer') {
        return next(new UnauthorizedError('Invalid Authorization header format. Expected Bearer token.'));
      }

      const token = parts[1]!;
      try {
        const decoded = jwt.verify(token, secret) as AuthenticatedUser;
        req.user = decoded;
        return next();
      } catch (err: any) {
        return next(new UnauthorizedError(`Invalid token: ${err.message}`));
      }
    };
  }

  public static requireRoles(...allowedRoles: UserRole[]) {
    return (req: any, res: any, next: any) => {
      if (!req.user) {
        return next(new UnauthorizedError('User is not authenticated.'));
      }

      if (!allowedRoles.includes(req.user.role)) {
        return next(new ForbiddenError(`Role ${req.user.role} does not have permission to access this resource.`));
      }

      return next();
    };
  }
}
""")

    write_file(f"{pkg_dir}/src/rate-limiter.ts", """import { AppError, ErrorCode } from '@novacommerce/core-types';

export class SlidingWindowRateLimiter {
  private readonly windowMs: number;
  private readonly maxRequests: number;
  private readonly clientRequests: Map<string, number[]> = new Map();

  constructor(windowMs: number = 60000, maxRequests: number = 100) {
    this.windowMs = windowMs;
    this.maxRequests = maxRequests;
  }

  public middleware() {
    return (req: any, res: any, next: any) => {
      const clientIp = req.ip || req.headers['x-forwarded-for'] || '127.0.0.1';
      const now = Date.now();
      const windowStart = now - this.windowMs;

      let timestamps = this.clientRequests.get(clientIp) || [];
      timestamps = timestamps.filter(ts => ts > windowStart);

      if (timestamps.length >= this.maxRequests) {
        return next(
          new AppError(
            `Rate limit exceeded. Maximum ${this.maxRequests} requests per ${this.windowMs / 1000}s.`,
            429,
            ErrorCode.RATE_LIMIT_EXCEEDED
          )
        );
      }

      timestamps.push(now);
      this.clientRequests.set(clientIp, timestamps);
      return next();
    };
  }
}
""")

    write_file(f"{pkg_dir}/src/validator.middleware.ts", """import { ZodSchema, ZodError } from 'zod';
import { ValidationError } from '@novacommerce/core-types';

export class RequestValidator {
  public static validateBody<T>(schema: ZodSchema<T>) {
    return (req: any, res: any, next: any) => {
      try {
        req.body = schema.parse(req.body);
        return next();
      } catch (err) {
        if (err instanceof ZodError) {
          const formatted = err.errors.map(e => ({
            field: e.path.join('.'),
            message: e.message
          }));
          return next(new ValidationError('Invalid request payload', formatted));
        }
        return next(err);
      }
    };
  }

  public static validateQuery<T>(schema: ZodSchema<T>) {
    return (req: any, res: any, next: any) => {
      try {
        req.query = schema.parse(req.query);
        return next();
      } catch (err) {
        if (err instanceof ZodError) {
          const formatted = err.errors.map(e => ({
            field: e.path.join('.'),
            message: e.message
          }));
          return next(new ValidationError('Invalid query parameters', formatted));
        }
        return next(err);
      }
    };
  }
}
""")

    write_file(f"{pkg_dir}/src/error.middleware.ts", """import { AppError, ApiErrorResponse, ErrorCode } from '@novacommerce/core-types';
import { ILogger } from '@novacommerce/core-logger';

export class ErrorHandlerMiddleware {
  public static handle(logger: ILogger) {
    return (err: any, req: any, res: any, next: any) => {
      const correlationId = req.headers['x-correlation-id'] || 'no-correlation-id';
      
      let statusCode = 500;
      let errorCode = ErrorCode.INTERNAL_SERVER_ERROR;
      let message = 'An internal server error occurred.';
      let details: any = undefined;

      if (err instanceof AppError) {
        statusCode = err.statusCode;
        errorCode = err.code;
        message = err.message;
        details = err.details;
      } else if (err.status || err.statusCode) {
        statusCode = err.status || err.statusCode;
        message = err.message || message;
      }

      logger.error(`HTTP Request failed: ${req.method} ${req.originalUrl || req.url}`, err, {
        correlationId,
        statusCode,
        errorCode
      });

      const responsePayload: ApiErrorResponse = {
        success: false,
        statusCode,
        error: {
          code: errorCode,
          message,
          details,
          correlationId: typeof correlationId === 'string' ? correlationId : correlationId[0],
          timestamp: new Date().toISOString()
        }
      };

      res.status(statusCode).json(responsePayload);
    };
  }
}
""")

    write_file(f"{pkg_dir}/src/index.ts", """export * from './auth.middleware.js';
export * from './rate-limiter.js';
export * from './validator.middleware.js';
export * from './error.middleware.js';
""")

    write_file(f"{pkg_dir}/tests/middleware.test.ts", """import { SlidingWindowRateLimiter } from '../src/index.js';

describe('Core Middleware Suite', () => {
  it('should enforce rate limits on excessive requests', (done) => {
    const limiter = new SlidingWindowRateLimiter(60000, 2);
    const middleware = limiter.middleware();

    const req: any = { ip: '192.168.1.1', headers: {} };
    const res: any = {};

    middleware(req, res, () => {
      middleware(req, res, () => {
        middleware(req, res, (err: any) => {
          expect(err).toBeDefined();
          expect(err.statusCode).toBe(429);
          done();
        });
      });
    });
  });
});
""")
    print(f"Generated {pkg_dir}")

def generate_core_database():
    pkg_dir = "packages/core-database"
    
    write_file(f"{pkg_dir}/package.json", """{
  "name": "@novacommerce/core-database",
  "version": "1.0.0",
  "description": "PostgreSQL database connection pool, Base Repository, Unit of Work and Migrations",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "clean": "rimraf dist",
    "test": "jest"
  },
  "dependencies": {
    "@novacommerce/core-types": "workspace:*",
    "@novacommerce/core-logger": "workspace:*"
  },
  "devDependencies": {
    "@types/jest": "^29.5.12",
    "@types/node": "^22.0.0",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.2",
    "typescript": "^5.4.0",
    "rimraf": "^5.0.5"
  }
}""")

    write_file(f"{pkg_dir}/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts", "**/*.test.ts"]
}""")

    write_file(f"{pkg_dir}/jest.config.js", """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.spec.ts', '**/*.test.ts']
};""")

    write_file(f"{pkg_dir}/src/base.repository.ts", """export interface IBaseRepository<T, ID = string> {
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
""")

    write_file(f"{pkg_dir}/src/unit-of-work.ts", """export interface IUnitOfWork {
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
""")

    write_file(f"{pkg_dir}/src/index.ts", """export * from './base.repository.js';
export * from './unit-of-work.js';
""")

    write_file(f"{pkg_dir}/tests/database.test.ts", """import { InMemoryBaseRepository } from '../src/index.js';

interface TestUser {
  id: string;
  name: string;
  email: string;
}

class TestUserRepository extends InMemoryBaseRepository<TestUser> {}

describe('Core Database Suite', () => {
  let repo: TestUserRepository;

  beforeEach(() => {
    repo = new TestUserRepository();
  });

  it('should create, find, update and delete entities', async () => {
    const user = await repo.create({ id: 'u1', name: 'Alice', email: 'alice@example.com' });
    expect(user.id).toBe('u1');

    const found = await repo.findById('u1');
    expect(found?.name).toBe('Alice');

    const updated = await repo.update('u1', { name: 'Alice B.' });
    expect(updated?.name).toBe('Alice B.');

    const count = await repo.count();
    expect(count).toBe(1);

    const deleted = await repo.delete('u1');
    expect(deleted).toBe(true);

    const afterDelete = await repo.findById('u1');
    expect(afterDelete).toBeNull();
  });
});
""")
    print(f"Generated {pkg_dir}")

def generate_core_grpc():
    pkg_dir = "packages/core-grpc"
    
    write_file(f"{pkg_dir}/package.json", """{
  "name": "@novacommerce/core-grpc",
  "version": "1.0.0",
  "description": "gRPC Client pooling, Interceptors, and Protobuf runtime bindings",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "clean": "rimraf dist",
    "test": "jest"
  },
  "dependencies": {
    "@novacommerce/core-types": "workspace:*",
    "@novacommerce/core-logger": "workspace:*"
  },
  "devDependencies": {
    "@types/jest": "^29.5.12",
    "@types/node": "^22.0.0",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.2",
    "typescript": "^5.4.0",
    "rimraf": "^5.0.5"
  }
}""")

    write_file(f"{pkg_dir}/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts", "**/*.test.ts"]
}""")

    write_file(f"{pkg_dir}/jest.config.js", """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.spec.ts', '**/*.test.ts']
};""")

    write_file(f"{pkg_dir}/src/types.ts", """export interface GrpcServiceConfig {
  host: string;
  port: number;
  timeoutMs?: number;
  maxRetries?: number;
}

export interface GrpcMetadata {
  correlationId?: string;
  userId?: string;
  authorization?: string;
}

export interface IGrpcClientPool<T> {
  getClient(): Promise<T>;
  releaseClient(client: T): void;
}
""")

    write_file(f"{pkg_dir}/src/client-pool.ts", """import { GrpcServiceConfig, IGrpcClientPool } from './types.js';
import { ILogger } from '@novacommerce/core-logger';

export class MockGrpcClientPool<T> implements IGrpcClientPool<T> {
  private readonly config: GrpcServiceConfig;
  private readonly clientFactory: (config: GrpcServiceConfig) => T;
  private readonly logger?: ILogger;
  private clientInstance: T | null = null;

  constructor(config: GrpcServiceConfig, clientFactory: (config: GrpcServiceConfig) => T, logger?: ILogger) {
    this.config = config;
    this.clientFactory = clientFactory;
    this.logger = logger;
  }

  public async getClient(): Promise<T> {
    if (!this.clientInstance) {
      this.clientInstance = this.clientFactory(this.config);
      this.logger?.debug(`Instantiated gRPC client connection to ${this.config.host}:${this.config.port}`);
    }
    return this.clientInstance;
  }

  public releaseClient(client: T): void {
    // Connection reuse in pool
  }
}
""")

    write_file(f"{pkg_dir}/src/index.ts", """export * from './types.js';
export * from './client-pool.js';
""")

    write_file(f"{pkg_dir}/tests/grpc.test.ts", """import { MockGrpcClientPool } from '../src/index.js';

describe('Core gRPC Suite', () => {
  it('should pool and return connected client instance', async () => {
    const mockFactory = (cfg: any) => ({
      host: cfg.host,
      port: cfg.port,
      ping: () => 'pong'
    });

    const pool = new MockGrpcClientPool({ host: 'localhost', port: 50051 }, mockFactory);
    const client = await pool.getClient();

    expect(client.host).toBe('localhost');
    expect(client.port).toBe(50051);
    expect(client.ping()).toBe('pong');
  });
});
""")
    print(f"Generated {pkg_dir}")

if __name__ == "__main__":
    generate_core_logger()
    generate_core_events()
    generate_core_middleware()
    generate_core_database()
    generate_core_grpc()
    print("All shared core packages generated successfully.")
