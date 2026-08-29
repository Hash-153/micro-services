export interface MetricTimeseriesPoint {
  timestamp: Date;
  metricName: string;
  value: number;
  tags: Record<string, string>;
}

export interface MetricAggregationSummary {
  metricName: string;
  count: number;
  sum: number;
  min: number;
  max: number;
  avg: number;
  p95: number;
  p99: number;
}

export class MetricsAggregator {
  private buffer: MetricTimeseriesPoint[] = [];

  public record(metricName: string, value: number, tags: Record<string, string> = {}): void {
    this.buffer.push({
      timestamp: new Date(),
      metricName,
      value,
      tags
    });
  }

  public aggregate(metricName: string, windowMs: number = 60000): MetricAggregationSummary {
    const cutoff = new Date(Date.now() - windowMs);
    const matching = this.buffer.filter(p => p.metricName === metricName && p.timestamp >= cutoff);

    if (matching.length === 0) {
      return {
        metricName,
        count: 0,
        sum: 0,
        min: 0,
        max: 0,
        avg: 0,
        p95: 0,
        p99: 0
      };
    }

    const values = matching.map(m => m.value).sort((a, b) => a - b);
    const sum = values.reduce((acc, v) => acc + v, 0);
    const count = values.length;
    const min = values[0];
    const max = values[values.length - 1];
    const avg = sum / count;
    const p95 = values[Math.floor(count * 0.95)] || max;
    const p99 = values[Math.floor(count * 0.99)] || max;

    return {
      metricName,
      count,
      sum,
      min,
      max,
      avg: Math.round(avg * 100) / 100,
      p95,
      p99
    };
  }

  public flushOldPoints(maxAgeMs: number = 3600000): void {
    const cutoff = new Date(Date.now() - maxAgeMs);
    this.buffer = this.buffer.filter(p => p.timestamp >= cutoff);
  }
}
