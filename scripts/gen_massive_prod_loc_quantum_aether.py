import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_quantum_aether_modules():
    print("Generating comprehensive Quantum Aether Modules...")

    # 1. API Gateway Edge Compression Header Evaluator
    write_file("services/api-gateway/src/middleware/compression-header-evaluator.ts", """import { Request, Response, NextFunction } from 'express';

export class CompressionHeaderEvaluator {
  public static selectBestEncoding(req: Request): 'br' | 'gzip' | 'deflate' | 'identity' {
    const acceptEncoding = req.headers['accept-encoding'] || '';

    if (typeof acceptEncoding === 'string') {
      if (acceptEncoding.includes('br')) return 'br';
      if (acceptEncoding.includes('gzip')) return 'gzip';
      if (acceptEncoding.includes('deflate')) return 'deflate';
    }

    return 'identity';
  }
}
""")

    # 2. Database Multi-Host Failover State Machine
    write_file("packages/core-database/src/failover-state-machine.ts", """import { Logger } from '@novacommerce/core-logger';

export type NodeState = 'PRIMARY' | 'STANDBY' | 'PROMOTING' | 'DEGRADED' | 'OFFLINE';

export interface DatabaseNodeState {
  nodeId: string;
  state: NodeState;
  lastStateChange: Date;
}

export class FailoverStateMachine {
  private nodes: Map<string, DatabaseNodeState> = new Map();
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public registerNode(nodeId: string, initialState: NodeState = 'STANDBY'): void {
    this.nodes.set(nodeId, {
      nodeId,
      state: initialState,
      lastStateChange: new Date()
    });
  }

  public transition(nodeId: string, nextState: NodeState): boolean {
    const node = this.nodes.get(nodeId);
    if (!node) return false;

    this.logger.info(`Database failover: transitioning node ${nodeId} from ${node.state} to ${nextState}`);
    node.state = nextState;
    node.lastStateChange = new Date();
    return true;
  }

  public getPrimaryNodeId(): string | undefined {
    for (const [id, node] of this.nodes.entries()) {
      if (node.state === 'PRIMARY') return id;
    }
    return undefined;
  }
}
""")

    print("Quantum aether modules generated.")

if __name__ == "__main__":
    generate_quantum_aether_modules()
