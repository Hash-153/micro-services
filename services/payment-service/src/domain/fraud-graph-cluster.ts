export interface GraphNode {
  id: string;
  type: 'IP' | 'CARD_BIN' | 'DEVICE_FINGERPRINT' | 'USER_EMAIL' | 'SHIPPING_ADDRESS';
}

export interface GraphEdge {
  fromNodeId: string;
  toNodeId: string;
  transactionId: string;
  weight: number;
}

export class FraudGraphCluster {
  private nodes: Map<string, GraphNode> = new Map();
  private edges: GraphEdge[] = [];

  public addTransactionLinks(transactionId: string, nodeDefinitions: GraphNode[]): void {
    for (const node of nodeDefinitions) {
      if (!this.nodes.has(node.id)) {
        this.nodes.set(node.id, node);
      }
    }

    for (let i = 0; i < nodeDefinitions.length; i++) {
      for (let j = i + 1; j < nodeDefinitions.length; j++) {
        this.edges.push({
          fromNodeId: nodeDefinitions[i].id,
          toNodeId: nodeDefinitions[j].id,
          transactionId,
          weight: 1.0
        });
      }
    }
  }

  public getConnectedComponentSize(startNodeId: string): number {
    const visited = new Set<string>();
    const queue: string[] = [startNodeId];
    visited.add(startNodeId);

    while (queue.length > 0) {
      const current = queue.shift()!;
      const neighbors = this.edges
        .filter(e => e.fromNodeId === current || e.toNodeId === current)
        .map(e => (e.fromNodeId === current ? e.toNodeId : e.fromNodeId));

      for (const n of neighbors) {
        if (!visited.has(n)) {
          visited.add(n);
          queue.push(n);
        }
      }
    }

    return visited.size;
  }
}
