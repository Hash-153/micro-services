export type LogLevel = 'debug' | 'info' | 'warn' | 'error' | 'fatal';

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
