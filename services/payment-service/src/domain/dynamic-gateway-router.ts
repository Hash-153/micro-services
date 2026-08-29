export interface GatewayHealthMetric {
  gatewayId: 'STRIPE' | 'PAYPAL' | 'ADYEN' | 'CHECKOUT_COM';
  successRatePercent: number;
  p95LatencyMs: number;
  interchangeMarkupBps: number;
  isDegraded: boolean;
}

export class DynamicGatewayRouter {
  public static selectOptimalGateway(metrics: GatewayHealthMetric[]): GatewayHealthMetric {
    // Filter healthy gateways
    const healthy = metrics.filter(m => !m.isDegraded && m.successRatePercent >= 98.0);
    const candidates = healthy.length > 0 ? healthy : metrics;

    // Sort by lowest cost markup, then latency
    return [...candidates].sort((a, b) => {
      if (a.interchangeMarkupBps !== b.interchangeMarkupBps) {
        return a.interchangeMarkupBps - b.interchangeMarkupBps;
      }
      return a.p95LatencyMs - b.p95LatencyMs;
    })[0];
  }
}
