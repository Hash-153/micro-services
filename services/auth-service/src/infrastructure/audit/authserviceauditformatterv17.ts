export interface AuditEventV17 {
  eventId: string;
  serviceName: 'auth-service';
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

export class AuthServiceAuditFormatterV17 {
  public static formatJson(event: AuditEventV17): string {
    return JSON.stringify({
      ...event,
      formattedTimestamp: event.timestamp.toISOString(),
      serviceScope: 'auth-service'
    });
  }

  public static formatSyslog(event: AuditEventV17): string {
    return `<134>1 ${event.timestamp.toISOString()} novacommerce auth-service - - [meta actor="${event.actorId}" role="${event.actorRole}"] Action ${event.action} on ${event.targetEntityType}:${event.targetEntityId} from ${event.ipAddress}`;
  }
}
