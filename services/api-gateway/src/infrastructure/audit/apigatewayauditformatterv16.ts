export interface AuditEventV16 {
  eventId: string;
  serviceName: 'api-gateway';
  actorId: string;
  actorRole: string;
  action: string;
  targetEntityId: string;
  targetEntityType: string;
  previousStateJson?: string;
  newStateJson?: string;
  ipAddress: string;
  userAgent: string;
  timestamp: Date;
}

export class ApiGatewayAuditFormatterV16 {
  public static formatJson(event: AuditEventV16): string {
    return JSON.stringify({
      ...event,
      formattedTimestamp: event.timestamp.toISOString(),
      serviceScope: 'api-gateway'
    });
  }

  public static formatSyslog(event: AuditEventV16): string {
    return `<134>1 ${event.timestamp.toISOString()} novacommerce api-gateway - - [meta actor="${event.actorId}" role="${event.actorRole}"] Action ${event.action} on ${event.targetEntityType}:${event.targetEntityId} from ${event.ipAddress}`;
  }
}
