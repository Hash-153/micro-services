import { Logger } from '@novacommerce/core-logger';

export interface TraceSpanContextV12 {
  traceId: string;
  spanId: string;
  parentSpanId?: string;
  serviceName: 'order-service';
  operationName: string;
  startTimeUnixNano: number;
  attributes: Record<string, string | number | boolean>;
  events: { name: string; timestampUnixNano: number; attributes?: Record<string, any> }[];
}

export class OrderServiceTracingInterceptorV12 {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public startSpan(operationName: string, parentContext?: Partial<TraceSpanContextV12>): TraceSpanContextV12 {
    const traceId = parentContext?.traceId || this.generateHexId(32);
    const spanId = this.generateHexId(16);

    const span: TraceSpanContextV12 = {
      traceId,
      spanId,
      parentSpanId: parentContext?.spanId,
      serviceName: 'order-service',
      operationName,
      startTimeUnixNano: Date.now() * 1000000,
      attributes: parentContext?.attributes || {},
      events: []
    };

    this.logger.info(`Started distributed trace span [${operationName}] (trace: ${traceId}, span: ${spanId}) in order-service`);
    return span;
  }

  public addEvent(span: TraceSpanContextV12, eventName: string, attributes?: Record<string, any>): void {
    span.events.push({
      name: eventName,
      timestampUnixNano: Date.now() * 1000000,
      attributes
    });
  }

  public endSpan(span: TraceSpanContextV12, isSuccess: boolean = true): void {
    const durationMs = (Date.now() * 1000000 - span.startTimeUnixNano) / 1000000;
    this.logger.info(`Ended trace span [${span.operationName}] duration=${durationMs.toFixed(2)}ms success=${isSuccess} in order-service`);
  }

  private generateHexId(length: number): string {
    let result = '';
    const hexChars = '0123456789abcdef';
    for (let i = 0; i < length; i++) {
      result += hexChars.charAt(Math.floor(Math.random() * hexChars.length));
    }
    return result;
  }
}
