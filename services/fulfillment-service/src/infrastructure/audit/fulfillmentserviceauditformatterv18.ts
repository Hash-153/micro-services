export interface AuditEventV18 {
  eventId: string;
  serviceName: 'fulfillment-service';
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

export class FulfillmentServiceAuditFormatterV18 {
  public static formatJson(event: AuditEventV18): string {
    return JSON.stringify({
      ...event,
      formattedTimestamp: event.timestamp.toISOString(),
      serviceScope: 'fulfillment-service'
    });
  }

  public static formatSyslog(event: AuditEventV18): string {
    return `<134>1 ${event.timestamp.toISOString()} novacommerce fulfillment-service - - [meta actor="${event.actorId}" role="${event.actorRole}"] Action ${event.action} on ${event.targetEntityType}:${event.targetEntityId} from ${event.ipAddress}`;
  }
}
