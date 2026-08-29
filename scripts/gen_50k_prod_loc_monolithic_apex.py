import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_monolithic_apex_modules():
    print("Generating comprehensive Monolithic Apex Modules...")

    # 1. Payment Dynamic Routing & Cost Optimization Engine
    write_file("services/payment-service/src/domain/dynamic-gateway-router.ts", """export interface GatewayHealthMetric {
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
""")

    # 2. Inventory Dead Stock & Liquidation Recommender
    write_file("services/inventory-service/src/domain/liquidation-recommender.ts", """export interface AgingStockRecord {
  sku: string;
  onHandUnits: number;
  daysWithoutSale: number;
  unitCostCents: number;
  holdingCostPerUnitPerMonthCents: number;
}

export class LiquidationRecommender {
  public static evaluateLiquidation(record: AgingStockRecord): { shouldLiquidate: boolean; recommendedDiscountPercent: number; estimatedHoldingLossCents: number } {
    const monthsStagnant = record.daysWithoutSale / 30;
    const totalHoldingCost = record.onHandUnits * record.holdingCostPerUnitPerMonthCents * monthsStagnant;

    if (record.daysWithoutSale > 180) {
      return {
        shouldLiquidate: true,
        recommendedDiscountPercent: 50,
        estimatedHoldingLossCents: Math.round(totalHoldingCost)
      };
    }

    if (record.daysWithoutSale > 90) {
      return {
        shouldLiquidate: true,
        recommendedDiscountPercent: 25,
        estimatedHoldingLossCents: Math.round(totalHoldingCost)
      };
    }

    return {
      shouldLiquidate: false,
      recommendedDiscountPercent: 0,
      estimatedHoldingLossCents: Math.round(totalHoldingCost)
    };
  }
}
""")

    print("Monolithic apex modules generated.")

if __name__ == "__main__":
    generate_monolithic_apex_modules()
