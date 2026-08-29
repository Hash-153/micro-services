export interface ServiceMetricPointV5 {
  metricName: string;
  serviceName: 'order-service';
  metricType: 'COUNTER' | 'GAUGE' | 'HISTOGRAM';
  value: number;
  tags: Record<string, string>;
  timestamp: Date;
}

export class OrderServiceTelemetryExporterV5 {
  private points: ServiceMetricPointV5[] = [];

  public recordMetric(metricName: string, value: number, metricType: ServiceMetricPointV5['metricType'] = 'COUNTER', tags: Record<string, string> = {}): void {
    this.points.push({
      metricName,
      serviceName: 'order-service',
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
      const formattedTags = tagStr ? `{service="order-service",${tagStr}}` : `{service="order-service"}`;
      lines.push(`${p.metricName}${formattedTags} ${p.value}`);
    }
    return lines.join('\n');
  }

  public flush(): void {
    this.points = [];
  }
}
