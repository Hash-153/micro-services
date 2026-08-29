export interface W3cTraceparent {
  version: string;
  traceId: string;
  parentId: string;
  traceFlags: string;
}

export class W3cTraceContextPropagator {
  public static parse(headerValue?: string): W3cTraceparent | null {
    if (!headerValue) return null;
    const parts = headerValue.trim().split('-');
    if (parts.length !== 4) return null;

    const [version, traceId, parentId, traceFlags] = parts;
    if (version !== '00') return null;
    if (traceId.length !== 32 || parentId.length !== 16) return null;

    return {
      version,
      traceId,
      parentId,
      traceFlags
    };
  }

  public static format(traceparent: W3cTraceparent): string {
    return `${traceparent.version}-${traceparent.traceId}-${traceparent.parentId}-${traceparent.traceFlags}`;
  }

  public static generate(): W3cTraceparent {
    const traceId = Array.from({ length: 32 }, () => Math.floor(Math.random() * 16).toString(16)).join('');
    const parentId = Array.from({ length: 16 }, () => Math.floor(Math.random() * 16).toString(16)).join('');
    return {
      version: '00',
      traceId,
      parentId,
      traceFlags: '01'
    };
  }
}
