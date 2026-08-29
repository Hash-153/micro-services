import { Logger } from '@novacommerce/core-logger';

export interface TraceSpanContextV11 {
  traceId: string;
  spanId: string;
  parentSpanId?: string;
  serviceName: 'inventory-service';
  operationName: string;
  startTimeUnixNano: number;
  attributes: Record<string, string | number | boolean>;
  events: { name: string; timestampUnixNano: number; attributes?: Record<string, any> }[];
}

export class InventoryServiceTracingInterceptorV11 {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public startSpan(operationName: string, parentContext?: Partial<TraceSpanContextV11>): TraceSpanContextV11 {
    const traceId = parentContext?.traceId || this.generateHexId(32);
    const spanId = this.generateHexId(16);

    const span: TraceSpanContextV11 = {
      traceId,
      spanId,
      parentSpanId: parentContext?.spanId,
      serviceName: 'inventory-service',
      operationName,
      startTimeUnixNano: Date.now() * 1000000,
      attributes: parentContext?.attributes || {},
      events: []
    };

    this.logger.info(`Started distributed trace span [${operationName}] (trace: ${traceId}, span: ${spanId}) in inventory-service`);
    return span;
  }

  public addEvent(span: TraceSpanContextV11, eventName: string, attributes?: Record<string, any>): void {
    span.events.push({
      name: eventName,
      timestampUnixNano: Date.now() * 1000000,
      attributes
    });
  }

  public endSpan(span: TraceSpanContextV11, isSuccess: boolean = true): void {
    const durationMs = (Date.now() * 1000000 - span.startTimeUnixNano) / 1000000;
    this.logger.info(`Ended trace span [${span.operationName}] duration=${durationMs.toFixed(2)}ms success=${isSuccess} in inventory-service`);
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
