import { ILogger, LogContext, LogEntry, LogLevel } from './types.js';
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
      process.stderr.write(outputJson + '\n');
    } else {
      process.stdout.write(outputJson + '\n');
    }
  }
}
