import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_quantum_scale():
    print("Generating comprehensive Production Quantum Scale Modules...")

    # 1. Payment Fraud Graph Clustering Engine
    write_file("services/payment-service/src/domain/fraud-graph-cluster.ts", """export interface GraphNode {
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
""")

    # 2. Inventory Automated Reorder Rule Trigger
    write_file("services/inventory-service/src/domain/auto-reorder-trigger.ts", """import { InventoryStockEntity } from '@novacommerce/core-types';

export interface AutoReorderDecision {
  sku: string;
  warehouseId: string;
  shouldTriggerReorder: boolean;
  orderQuantity: number;
  reason: string;
}

export class AutoReorderTrigger {
  public static evaluateStock(stock: InventoryStockEntity): AutoReorderDecision {
    const effectiveStock = stock.onHandQuantity - stock.reservedQuantity;
    const isBelowSafety = effectiveStock <= stock.safetyStockThreshold;

    if (isBelowSafety) {
      return {
        sku: stock.sku,
        warehouseId: stock.warehouseId,
        shouldTriggerReorder: true,
        orderQuantity: stock.reorderQuantity,
        reason: `Available stock (${effectiveStock}) breached safety stock threshold (${stock.safetyStockThreshold}).`
      };
    }

    return {
      sku: stock.sku,
      warehouseId: stock.warehouseId,
      shouldTriggerReorder: false,
      orderQuantity: 0,
      reason: 'Stock levels within normal operating buffer.'
    };
  }
}
""")

    print("Production quantum scale modules generated.")

if __name__ == "__main__":
    generate_prod_quantum_scale()
