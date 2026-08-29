import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_master_titan_modules():
    print("Generating comprehensive Master Titan Modules...")

    # 1. SQL Query Builder AST Node Formatter
    write_file("packages/core-database/src/query-ast-formatter.ts", """export type SqlOperator = '=' | '!=' | '>' | '>=' | '<' | '<=' | 'LIKE' | 'ILIKE' | 'IN' | 'NOT IN' | 'IS NULL' | 'IS NOT NULL';

export interface SqlConditionNode {
  type: 'CONDITION';
  field: string;
  operator: SqlOperator;
  value?: any;
}

export interface SqlLogicalNode {
  type: 'LOGICAL';
  operator: 'AND' | 'OR' | 'NOT';
  children: (SqlConditionNode | SqlLogicalNode)[];
}

export class QueryAstFormatter {
  public static formatCondition(node: SqlConditionNode | SqlLogicalNode, params: any[]): string {
    if (node.type === 'CONDITION') {
      if (node.operator === 'IS NULL' || node.operator === 'IS NOT NULL') {
        return `"${node.field}" ${node.operator}`;
      }

      if (node.operator === 'IN' || node.operator === 'NOT IN') {
        if (!Array.isArray(node.value) || node.value.length === 0) {
          return node.operator === 'IN' ? '1=0' : '1=1';
        }
        const placeholders = node.value.map(v => {
          params.push(v);
          return `$${params.length}`;
        });
        return `"${node.field}" ${node.operator} (${placeholders.join(', ')})`;
      }

      params.push(node.value);
      return `"${node.field}" ${node.operator} $${params.length}`;
    }

    if (node.type === 'LOGICAL') {
      if (node.operator === 'NOT') {
        const childStr = this.formatCondition(node.children[0], params);
        return `NOT (${childStr})`;
      }

      const formattedChildren = node.children.map(c => this.formatCondition(c, params));
      return `(${formattedChildren.join(` ${node.operator} `)})`;
    }

    return '1=1';
  }
}
""")

    # 2. OpenTelemetry Prometheus Metrics Exporter
    write_file("packages/core-logger/src/prometheus-metrics-exporter.ts", """export interface PrometheusMetricEntry {
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

    return lines.join('\\n');
  }
}
""")

    print("Master titan modules generated.")

if __name__ == "__main__":
    generate_master_titan_modules()
