export interface ReadReplicaNode {
  host: string;
  port: number;
  weight: number;
  currentActiveConnections: number;
  isHealthy: boolean;
}

export class ReplicaWeightedDispatcher {
  private replicas: ReadReplicaNode[];
  private currentIndex: number = 0;

  constructor(replicas: ReadReplicaNode[]) {
    this.replicas = replicas;
  }

  public getNextHealthyReplica(): ReadReplicaNode | null {
    const healthy = this.replicas.filter(r => r.isHealthy);
    if (healthy.length === 0) return null;

    // Weighted least connections
    return [...healthy].sort((a, b) => {
      const loadA = a.currentActiveConnections / a.weight;
      const loadB = b.currentActiveConnections / b.weight;
      return loadA - loadB;
    })[0];
  }
}
