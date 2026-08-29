export interface FacilityCapacitySnapshot {
  warehouseId: string;
  currentActivePicksCount: number;
  maxPickThroughputPerHour: number;
  utilizationPercentage: number;
}

export class FacilityLoadBalancer {
  public static selectLeastLoadedFacility(facilities: FacilityCapacitySnapshot[]): FacilityCapacitySnapshot | null {
    if (facilities.length === 0) return null;

    return [...facilities].sort((a, b) => {
      // Choose lowest utilization percentage
      return a.utilizationPercentage - b.utilizationPercentage;
    })[0];
  }
}
