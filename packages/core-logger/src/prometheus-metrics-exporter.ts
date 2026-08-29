export interface PrometheusMetricEntry {
  name: string;
  type: 'counter' | 'gauge' | 'histogram';
  help: string;
  labels: Record<string, string>;
  value: number;
}

export class PrometheusMetricsExporter {
  private metrics: Map<string, PrometheusMetricEntry> = new Map();

  public setMetric(entry: PrometheusMetricEntry): void {
    const labelKey = Object.entries(entry.labels)
      .sort((a, b) => a[0].localeCompare(b[0]))
      .map(([k, v]) => `${k}="${v}"`)
      .join(',');

    const key = `${entry.name}{${labelKey}}`;
    this.metrics.set(key, entry);
  }

  public exportPrometheusFormat(): string {
    const lines: string[] = [];
    const groupedByName = new Map<string, PrometheusMetricEntry[]>();

    for (const m of this.metrics.values()) {
      if (!groupedByName.has(m.name)) {
        groupedByName.set(m.name, []);
      }
      groupedByName.get(m.name)!.push(m);
    }

    for (const [name, list] of groupedByName.entries()) {
      const first = list[0];
      lines.push(`# HELP ${name} ${first.help}`);
      lines.push(`# TYPE ${name} ${first.type}`);

      for (const item of list) {
        const labelPairs = Object.entries(item.labels)
          .map(([k, v]) => `${k}="${v}"`)
          .join(',');
        const labelsStr = labelPairs ? `{${labelPairs}}` : '';
        lines.push(`${item.name}${labelsStr} ${item.value}`);
      }
      lines.push('');
    }

    return lines.join('\n');
  }
}
