export type SqlOperator = '=' | '!=' | '>' | '>=' | '<' | '<=' | 'LIKE' | 'ILIKE' | 'IN' | 'NOT IN' | 'IS NULL' | 'IS NOT NULL';

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
