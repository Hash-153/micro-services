import { Logger } from '@novacommerce/core-logger';

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
