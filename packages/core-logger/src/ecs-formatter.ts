export interface EcsLogEntry {
  '@timestamp': string;
  'log.level': string;
  message: string;
  'service.name': string;
  'service.version': string;
  'trace.id'?: string;
  'transaction.id'?: string;
  'error.type'?: string;
  'error.message'?: string;
  'error.stack_trace'?: string;
  custom?: Record<string, any>;
}

export class EcsLogFormatter {
  private serviceName: string;
  private serviceVersion: string;

  constructor(serviceName: string, serviceVersion: string = '1.0.0') {
    this.serviceName = serviceName;
    this.serviceVersion = serviceVersion;
  }

  public format(level: string, message: string, context?: Record<string, any>, error?: Error): string {
    const entry: EcsLogEntry = {
      '@timestamp': new Date().toISOString(),
      'log.level': level.toUpperCase(),
      message,
      'service.name': this.serviceName,
      'service.version': this.serviceVersion,
      'trace.id': context?.traceId,
      'transaction.id': context?.transactionId
    };

    if (error) {
      entry['error.type'] = error.name;
      entry['error.message'] = error.message;
      entry['error.stack_trace'] = error.stack;
    }

    if (context) {
      const { traceId, transactionId, ...rest } = context;
      if (Object.keys(rest).length > 0) {
        entry.custom = rest;
      }
    }

    return JSON.stringify(entry);
  }
}
