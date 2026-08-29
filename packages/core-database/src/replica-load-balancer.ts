import { Logger } from '@novacommerce/core-logger';

export interface DatabaseNode {
  nodeId: string;
  host: string;
  port: number;
  isMaster: boolean;
  weight: number;
  activeConnections: number;
}

export class ReplicaLoadBalancer {
  private logger: Logger;
  private nodes: DatabaseNode[] = [];
  private roundRobinIndex: number = 0;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public registerNode(node: DatabaseNode): void {
    this.nodes.push(node);
    this.logger.info(`Database node registered: ${node.nodeId} (${node.host}:${node.port}, isMaster=${node.isMaster})`);
  }

  public getMaster(): DatabaseNode {
    const master = this.nodes.find(n => n.isMaster);
    if (!master) throw new Error('No master database node registered');
    return master;
  }

  public getReadReplica(): DatabaseNode {
    const replicas = this.nodes.filter(n => !n.isMaster);
    if (replicas.length === 0) {
      return this.getMaster(); // Fallback to master
    }

    const selected = replicas[this.roundRobinIndex % replicas.length];
    this.roundRobinIndex++;
    return selected;
  }
}
