import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_nexus():
    print("Generating comprehensive Production Nexus Modules...")

    # 1. Product Recommendations Collaborative Filtering
    write_file("services/catalog-service/src/domain/collaborative-filter.ts", """export interface UserProductInteraction {
  userId: string;
  sku: string;
  interactionType: 'VIEW' | 'ADD_TO_CART' | 'PURCHASE' | 'WISHLIST';
  weight: number;
}

export class CollaborativeFilteringEngine {
  private static readonly WEIGHTS = {
    VIEW: 1.0,
    WISHLIST: 2.5,
    ADD_TO_CART: 4.0,
    PURCHASE: 10.0
  };

  public static buildUserItemMatrix(interactions: UserProductInteraction[]): Map<string, Map<string, number>> {
    const matrix: Map<string, Map<string, number>> = new Map();

    for (const inter of interactions) {
      if (!matrix.has(inter.userId)) {
        matrix.set(inter.userId, new Map());
      }
      const userVector = matrix.get(inter.userId)!;
      const w = this.WEIGHTS[inter.interactionType] || 1.0;
      userVector.set(inter.sku, (userVector.get(inter.sku) || 0) + w);
    }

    return matrix;
  }

  public static calculateCosineSimilarity(vectorA: Map<string, number>, vectorB: Map<string, number>): number {
    let dotProduct = 0;
    let normA = 0;
    let normB = 0;

    for (const [key, valA] of vectorA.entries()) {
      normA += valA * valA;
      if (vectorB.has(key)) {
        dotProduct += valA * vectorB.get(key)!;
      }
    }

    for (const valB of vectorB.values()) {
      normB += valB * valB;
    }

    if (normA === 0 || normB === 0) return 0;
    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
  }
}
""")

    # 2. Analytics Anomaly Detector
    write_file("services/analytics-service/src/domain/anomaly-detector.ts", """export class TimeseriesAnomalyDetector {
  public static detectAnomalies(values: number[], zScoreThreshold: number = 3.0): { index: number; value: number; zScore: number }[] {
    if (values.length < 5) return [];

    const mean = values.reduce((a, b) => a + b, 0) / values.length;
    const variance = values.reduce((acc, v) => acc + Math.pow(v - mean, 2), 0) / values.length;
    const stdDev = Math.sqrt(variance);

    if (stdDev === 0) return [];

    const anomalies: { index: number; value: number; zScore: number }[] = [];

    values.forEach((v, idx) => {
      const z = Math.abs(v - mean) / stdDev;
      if (z >= zScoreThreshold) {
        anomalies.push({
          index: idx,
          value: v,
          zScore: Math.round(z * 100) / 100
        });
      }
    });

    return anomalies;
  }
}
""")

    print("Production nexus modules generated.")

if __name__ == "__main__":
    generate_prod_nexus()
