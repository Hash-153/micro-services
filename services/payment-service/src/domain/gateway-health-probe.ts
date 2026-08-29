import { Logger } from '@novacommerce/core-logger';

export interface GatewayHealthStatus {
  gatewayName: string;
  isHealthy: boolean;
  latencyMs: number;
  lastCheckedAt: Date;
  consecutiveFailures: number;
}

export class GatewayHealthProbe {
  private logger: Logger;
  private statusMap: Map<string, GatewayHealthStatus> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async probeGateway(gatewayName: string, pingFn: () => Promise<void>): Promise<GatewayHealthStatus> {
    const start = Date.now();
    let isHealthy = false;
    let consecutiveFailures = (this.statusMap.get(gatewayName)?.consecutiveFailures || 0);

    try {
      await pingFn();
      isHealthy = true;
      consecutiveFailures = 0;
    } catch (error) {
      isHealthy = false;
      consecutiveFailures++;
      this.logger.warn(`Gateway health probe failed for ${gatewayName} (failure #${consecutiveFailures})`);
    }

    const latencyMs = Date.now() - start;
    const status: GatewayHealthStatus = {
      gatewayName,
      isHealthy,
      latencyMs,
      lastCheckedAt: new Date(),
      consecutiveFailures
    };

    this.statusMap.set(gatewayName, status);
    return status;
  }

  public getStatus(gatewayName: string): GatewayHealthStatus | undefined {
    return this.statusMap.get(gatewayName);
  }
}
