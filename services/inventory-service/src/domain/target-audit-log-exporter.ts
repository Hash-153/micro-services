export interface TargetAuditLogEntry {
  sku: string;
  previousSafetyStock: number;
  newSafetyStock: number;
  reason: string;
  timestamp: Date;
}

export class TargetAuditLogExporter {
  public static exportCsv(entries: TargetAuditLogEntry[]): string {
    const header = 'SKU,PreviousSafetyStock,NewSafetyStock,Reason,Timestamp';
    const rows = entries.map(e => `${e.sku},${e.previousSafetyStock},${e.newSafetyStock},"${e.reason}",${e.timestamp.toISOString()}`);
    return [header, ...rows].join('\n');
  }
}
