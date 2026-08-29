export interface ServiceMetricPointV4 {
  metricName: string;
  serviceName: 'fulfillment-service';
  metricType: 'COUNTER' | 'GAUGE' | 'HISTOGRAM';
  value: number;
  tags: Record<string, string>;
  timestamp: Date;
}

export class FulfillmentServiceTelemetryExporterV4 {
  private points: ServiceMetricPointV4[] = [];

  public recordMetric(metricName: string, value: number, metricType: ServiceMetricPointV4['metricType'] = 'COUNTER', tags: Record<string, string> = {}): void {
    this.points.push({
      metricName,
      serviceName: 'fulfillment-service',
      metricType,
      value,
      tags,
      timestamp: new Date()
    });
  }

  public exportOpenMetrics(): string {
    const lines: string[] = [];
    for (const p of this.points) {
      const tagStr = Object.entries(p.tags).map(([k, v]) => `${k}="${v}"`).join(',');
      const formattedTags = tagStr ? `{service="fulfillment-service",${tagStr}}` : `{service="fulfillment-service"}`;
      lines.push(`${p.metricName}${formattedTags} ${p.value}`);
    }
    return lines.join('\n');
  }

  public flush(): void {
    this.points = [];
  }
}
