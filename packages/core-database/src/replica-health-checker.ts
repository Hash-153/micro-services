import { Logger } from '@novacommerce/core-logger';
import { DatabaseNode } from './replica-load-balancer.js';

export class ReplicaHealthChecker {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async checkNode(node: DatabaseNode): Promise<{ isReachable: boolean; replicationLagSeconds: number }> {
    try {
      // In production queries 'SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp())) AS lag'
      return {
        isReachable: true,
        replicationLagSeconds: 0.05
      };
    } catch (error) {
      this.logger.error(`Database replica node ${node.nodeId} health check failed`);
      return {
        isReachable: false,
        replicationLagSeconds: 999999
      };
    }
  }
}
