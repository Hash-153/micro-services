export interface WarehouseLocation {
  warehouseId: string;
  code: string;
  name: string;
  latitude: number;
  longitude: number;
  availableStock: number;
}

export interface DeliveryDestination {
  latitude: number;
  longitude: number;
  countryCode: string;
  postalCode: string;
}

export class WarehouseRoutingService {
  // Selects nearest warehouse with adequate stock using Haversine distance
  public static selectOptimalWarehouse(
    destination: DeliveryDestination,
    warehouses: WarehouseLocation[],
    requiredQuantity: number
  ): WarehouseLocation | null {
    const eligible = warehouses.filter(w => w.availableStock >= requiredQuantity);
    if (eligible.length === 0) return null;

    let closestWarehouse: WarehouseLocation | null = null;
    let shortestDistanceKm = Infinity;

    for (const wh of eligible) {
      const dist = this.haversineDistanceKm(
        destination.latitude,
        destination.longitude,
        wh.latitude,
        wh.longitude
      );

      if (dist < shortestDistanceKm) {
        shortestDistanceKm = dist;
        closestWarehouse = wh;
      }
    }

    return closestWarehouse;
  }

  private static haversineDistanceKm(lat1: number, lon1: number, lat2: number, lon2: number): number {
    const R = 6371; // Earth radius in km
    const dLat = this.toRadians(lat2 - lat1);
    const dLon = this.toRadians(lon2 - lon1);
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(this.toRadians(lat1)) * Math.cos(this.toRadians(lat2)) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }

  private static toRadians(deg: number): number {
    return deg * (Math.PI / 180);
  }
}
