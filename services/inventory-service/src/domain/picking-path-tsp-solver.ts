export interface WarehousePickLocation {
  binId: string;
  xCoordMeters: number;
  yCoordMeters: number;
}

export class PickingPathTspSolver {
  public static solvePickSequence(startLocation: WarehousePickLocation, pickLocations: WarehousePickLocation[]): WarehousePickLocation[] {
    const unvisited = [...pickLocations];
    const sequence: WarehousePickLocation[] = [];
    let current = startLocation;

    while (unvisited.length > 0) {
      // Find nearest neighbor
      let nearestIdx = 0;
      let minDistance = Infinity;

      for (let i = 0; i < unvisited.length; i++) {
        const candidate = unvisited[i];
        const dist = Math.hypot(candidate.xCoordMeters - current.xCoordMeters, candidate.yCoordMeters - current.yCoordMeters);
        if (dist < minDistance) {
          minDistance = dist;
          nearestIdx = i;
        }
      }

      const nextPick = unvisited.splice(nearestIdx, 1)[0];
      sequence.push(nextPick);
      current = nextPick;
    }

    return sequence;
  }
}
