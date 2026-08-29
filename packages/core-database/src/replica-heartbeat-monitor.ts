import { Logger } from '@novacommerce/core-logger';

export interface DatabaseNodeHeartbeat {
  nodeId: string;
  host: string;
  replicationLagSeconds: number;
  isReadOnly: boolean;
  lastHeartbeat: Date;
}

export class ReplicaHeartbeatMonitor {
  private nodes: Map<string, DatabaseNodeHeartbeat> = new Map();
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public recordHeartbeat(heartbeat: DatabaseNodeHeartbeat): void {
    this.nodes.set(heartbeat.nodeId, heartbeat);
    if (heartbeat.replicationLagSeconds > 10) {
      this.logger.warn(`Replica node ${heartbeat.nodeId} (${heartbeat.host}) experiencing high lag: ${heartbeat.replicationLagSeconds}s`);
    }
  }

  public getAvailableReplicaIds(maxAllowableLagSeconds: number = 5): string[] {
    const valid: string[] = [];
    const now = Date.now();

    for (const [id, node] of this.nodes.entries()) {
      const isFresh = now - node.lastHeartbeat.getTime() < 15000;
      if (isFresh && node.replicationLagSeconds <= maxAllowableLagSeconds) {
        valid.push(id);
      }
    }

    return valid;
  }
}
