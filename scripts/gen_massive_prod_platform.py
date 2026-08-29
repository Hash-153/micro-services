import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def build_notification_and_analytics():
    print("Building Notification and Analytics domain expanded...")
    
    # 1. Template Compiler
    write_file("services/notification-service/src/domain/template-compiler.ts", """export class TemplateCompiler {
  public static compile(templateString: string, variables: Record<string, any>): string {
    let result = templateString;
    for (const [key, value] of Object.entries(variables)) {
      const regex = new RegExp(`{{\\s*${key}\\s*}}`, 'g');
      result = result.replace(regex, String(value ?? ''));
    }
    return result;
  }

  public static sanitizeHtml(html: string): string {
    return html
      .replace(/<script\\b[^<]*(?:(?!<\\/script>)<[^<]*)*<\\/script>/gi, '')
      .replace(/on\\w+="[^"]*"/g, '')
      .replace(/javascript:[^"']*/g, '');
  }
}
""")

    # 2. Conversion Funnel Service
    write_file("services/analytics-service/src/services/conversion-funnel.service.ts", """import { ConversionFunnelStep, ClickstreamEventPayload } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export class ConversionFunnelService {
  private logger: Logger;
  private rawEvents: ClickstreamEventPayload[] = [];

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public recordEvent(event: ClickstreamEventPayload): void {
    this.rawEvents.push(event);
  }

  public computeFunnel(steps: { stepName: string; eventName: string }[]): ConversionFunnelStep[] {
    const funnel: ConversionFunnelStep[] = [];
    let previousCount = 0;
    let initialCount = 0;

    for (let i = 0; i < steps.length; i++) {
      const step = steps[i];
      // Count unique sessions that performed this event
      const matchingSessions = new Set(
        this.rawEvents
          .filter(e => e.eventName === step.eventName && e.sessionId)
          .map(e => e.sessionId as string)
      );

      const count = matchingSessions.size;

      if (i === 0) {
        initialCount = count;
        previousCount = count;
      }

      const conversionFromPrev = previousCount > 0 ? Math.round((count / previousCount) * 1000) / 10 : 0;
      const overallDropoff = initialCount > 0 ? Math.round(((initialCount - count) / initialCount) * 1000) / 10 : 0;

      funnel.push({
        stepIndex: i + 1,
        stepName: step.stepName,
        eventName: step.eventName,
        uniqueUsers: count,
        conversionRateFromPrevious: conversionFromPrev,
        overallDropoffRate: overallDropoff
      });

      previousCount = count;
    }

    return funnel;
  }
}
""")

    # 3. Audit Trail Exporter
    write_file("services/analytics-service/src/services/audit-exporter.service.ts", """import { AuditLogEntity } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export interface AuditExportFilter {
  serviceName?: string;
  actorId?: string;
  resourceType?: string;
  resourceId?: string;
  fromDate?: Date;
  toDate?: Date;
}

export class AuditExporterService {
  private logger: Logger;
  private auditLogs: AuditLogEntity[] = [];

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public logAudit(entry: Omit<AuditLogEntity, 'id' | 'timestamp'>): AuditLogEntity {
    const record: AuditLogEntity = {
      ...entry,
      id: crypto.randomUUID(),
      timestamp: new Date()
    };
    this.auditLogs.push(record);
    return record;
  }

  public exportCsv(filter: AuditExportFilter = {}): string {
    const filtered = this.auditLogs.filter(log => {
      if (filter.serviceName && log.serviceName !== filter.serviceName) return false;
      if (filter.actorId && log.actorId !== filter.actorId) return false;
      if (filter.resourceType && log.resourceType !== filter.resourceType) return false;
      if (filter.fromDate && log.timestamp < filter.fromDate) return false;
      if (filter.toDate && log.timestamp > filter.toDate) return false;
      return true;
    });

    const headers = ['id', 'timestamp', 'service_name', 'action', 'actor_id', 'actor_role', 'resource_type', 'resource_id'];
    const rows = filtered.map(log => [
      log.id,
      log.timestamp.toISOString(),
      `"${log.serviceName}"`,
      `"${log.action}"`,
      `"${log.actorId}"`,
      `"${log.actorRole}"`,
      `"${log.resourceType}"`,
      `"${log.resourceId}"`
    ].join(','));

    return [headers.join(','), ...rows].join('\\n');
  }
}
""")

    print("Notification & Analytics domain expanded.")

if __name__ == "__main__":
    build_notification_and_analytics()
