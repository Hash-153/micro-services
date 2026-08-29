import { PickItem, AisleGraphOptimizer } from './aisle-graph-optimizer.js';

export interface PickWave {
  waveId: string;
  assignedPickerId?: string;
  totalItemsCount: number;
  distinctSkusCount: number;
  items: PickItem[];
  estimatedPickDurationMinutes: number;
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED';
}

export class BatchPickPlanner {
  public static planWave(orderItems: { orderId: string; sku: string; quantity: number; binLocation: any }[], maxItemsPerWave: number = 50): PickWave[] {
    const waves: PickWave[] = [];
    const pickItems: PickItem[] = orderItems.map(it => ({
      sku: it.sku,
      quantity: it.quantity,
      binLocation: it.binLocation
    }));

    // Optimize entire picking trajectory
    const optimizedItems = AisleGraphOptimizer.calculateOptimalPickPath(pickItems);

    for (let i = 0; i < optimizedItems.length; i += maxItemsPerWave) {
      const chunk = optimizedItems.slice(i, i + maxItemsPerWave);
      const waveId = `wave_${Date.now().toString(36)}_${Math.floor(i / maxItemsPerWave) + 1}`;
      const totalUnits = chunk.reduce((acc, it) => acc + it.quantity, 0);
      const distinctSkus = new Set(chunk.map(it => it.sku)).size;

      waves.push({
        waveId,
        totalItemsCount: totalUnits,
        distinctSkusCount: distinctSkus,
        items: chunk,
        estimatedPickDurationMinutes: Math.ceil(totalUnits * 0.75), // 45s per pick estimate
        status: 'PENDING'
      });
    }

    return waves;
  }
}
