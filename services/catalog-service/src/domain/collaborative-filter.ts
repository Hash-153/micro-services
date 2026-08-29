export interface UserProductInteraction {
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
